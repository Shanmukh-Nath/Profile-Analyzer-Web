from django.db.models import Count, Sum
from random import sample

from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.clickjacking import xframe_options_exempt
from questions_app.models import Question, Applicant, UserAnswer, Answer, Resume, IQQuestion
from questions_app.serializers import QuestionSerializer, ApplicantSerializer, IQQuestionSerializer


@xframe_options_exempt
def applicant_profile(request, applicant_id):
    applicant = get_object_or_404(Applicant, id=applicant_id)
    url = applicant.github_link
    username = url.split('/')[-1]
    linkid = applicant.linkedin_link
    link = linkid.split('/')[-1]
    print(link)
    overall = applicant.overall_score
    tech_score = applicant.tech_score
    sales = applicant.sales_score
    iq = applicant.iq_score
    cert = send_certs(link)
    most = git_most(username)
    domain = applicant.domain_suitability
    return render(request, 'applicant_profile.html', {'applicant': applicant,'most':most,'link':cert,'overall':overall,'tech_score':tech_score,'sales_score':sales,'iq':iq,'domain':domain})
def index(request):
    applicants = Applicant.objects.all()
    return render(request,'index.html',{'applicants':applicants})


import requests

def send_certs(id):
    import requests
    url = "https://api.scrapingdog.com/linkedin/"
    params = {
        "api_key": "653de9ddf5c3d932a0812683",
        "type": "profile",
        "linkId": id
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        to_frontend_linkedin_cert=[]
        for i in range(len(data[0]['certification'])):
            to_frontend_linkedin_cert.append(data[0]['certification'][i]['certification'])
        return to_frontend_linkedin_cert
    else:
        return str(f"Request failed with status code: {response.status_code}")



def git_most(username):
    def get_repositories(username):
        repos_api_url = f"https://api.github.com/users/{username}/repos?per_page=100"
        headers = {
            'Authorization': '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',
            'Accept': 'application/vnd.github.v3+json',
        }

        response = requests.get(repos_api_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve repositories for {username}. Status code: {response.status_code}")
            return []


    def get_primary_language_for_repo(repo_data):
        if not repo_data.get("fork"):  # Exclude forked repositories
            return repo_data.get("language")

    username = "nprashanthvarma"  # Replace with the target username
    repositories = get_repositories(username)

    languages = [get_primary_language_for_repo(repo) for repo in repositories]
    languages = [lang for lang in languages if lang]  # Filter out None

    # Count the occurrences of each language
    language_counts = {}
    for lang in languages:
        language_counts[lang] = language_counts.get(lang, 0) + 1

    # Determine the most frequently used language
    most_used_language = max(language_counts, key=language_counts.get)
    return most_used_language


class RandomQuestionList(APIView):
    def get(self, request):
        question_types = Question.objects.values('question_type').annotate(count=Count('question_type')).values(
            'question_type')
        iq_questions_types = IQQuestion.objects.values('question_type').annotate(count=Count('question_type')).values(
            'question_type')

        random_question_objects = []
        random_iq_question_objects = []

        for q_type in question_types:
            questions_for_type = Question.objects.filter(question_type=q_type['question_type'])
            random_question_objects.extend(sample(list(questions_for_type), 5))

        for q_type in iq_questions_types:
            iq_questions_for_type = IQQuestion.objects.filter(question_type=q_type['question_type'])
            random_iq_question_objects.extend(sample(list(iq_questions_for_type), 2))

        question_serializer = QuestionSerializer(random_question_objects, many=True)
        iq_question_serializer = IQQuestionSerializer(random_iq_question_objects, many=True)

        # Combine the data from both serializers for the final output
        combined_data = question_serializer.data + iq_question_serializer.data

        return Response(combined_data)


def evaluate_applicant_scores(applicant, tech_score, sales_score, iq_score):
    applicant.tech_score = tech_score
    applicant.sales_score = sales_score
    applicant.iq_score = iq_score
    applicant.domain_suitability = 'tech' if tech_score > sales_score else 'sales'
    if tech_score>sales_score:
        main_score = tech_score
    else:
        main_score = sales_score
    total_score = tech_score+sales_score
    formula = (total_score * 0.5) + (iq_score*0.5)
    applicant.overall_score = formula
    applicant.save()


class SaveAnswer(APIView):
    def post(self, request):
        # Get the applicant by email
        try:
            applicant = Applicant.objects.get(email=request.data['email'])
        except Applicant.DoesNotExist:
            return Response({"error": "Applicant not found"}, status=status.HTTP_400_BAD_REQUEST)

        answers = request.data['answers']
        tech_score = 0
        sales_score = 0
        iq_score = 0
        print(request.data)
        # Loop through the answers dictionary
        for question_id, selected_option_text in answers.items():
            try:
                question = Question.objects.get(id=question_id)
                model = "main"
            except Question.DoesNotExist:
                try:
                    question = IQQuestion.objects.get(id=question_id)
                    model = "iq"
                except IQQuestion.DoesNotExist:
                    print(f"Question with ID {question_id} does not exist")
                    continue  # If not found in both, skip this iteration

            # Determine the index of the selected option
            for i in range(1, 5):  # assuming max 4 options; adjust if different
                option_field = f"option_{i}"
                if getattr(question, option_field) == selected_option_text:
                    selected_option = i
                    break
            else:
                print(f"No matching option found for Question ID {question_id}")
                continue  # skip this iteration and process the next answer

            points_field = f"option_{selected_option}_ps"
            points_awarded = getattr(question, points_field, 0)

            # Add points to respective score based on question type
            if model == "main":
                if question.question_type == "Tech":
                    tech_score += points_awarded
                else:  # Assuming only two types: tech and sales
                    sales_score += points_awarded
            elif model == "iq":
                iq_score += points_awarded

            UserAnswer.objects.create(
                applicant=applicant,
                question=question,
                selected_option=selected_option,
                points_awarded=points_awarded
            )

        # Evaluate scores for the applicant
        evaluate_applicant_scores(applicant, tech_score, sales_score, iq_score)

        return Response({"message": "Answers saved successfully"}, status=status.HTTP_201_CREATED)



class ApplicantProfile(APIView):
    def post(self, request):
        applicant, created = Applicant.objects.get_or_create(email=request.data['email'], defaults=request.data)
        if not created:
            serializer = ApplicantSerializer(applicant, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Profile created successfully"}, status=status.HTTP_201_CREATED)


class SubmitSocials(APIView):
    def post(self,request):
        email = request.data['email']
        applicant = Applicant.objects.get(email=email)
        socials = request.data['socials']
        applicant.facebook_link = socials['facebook']
        applicant.instagram_link = socials['instagram']
        applicant.leetcode_link = socials['leetcode']
        applicant.github_link = socials['github']
        applicant.linkedin_link = socials['linkedin']
        applicant.save()

        return Response({"message": "Resume uploaded successfully"}, status=status.HTTP_200_OK)

class UploadResume(APIView):
    def post(self, request):
        applicant_email = request.data.get('email')
        try:
            applicant = Applicant.objects.get(email=applicant_email)
        except Applicant.DoesNotExist:
            return Response({"error": "Applicant not found"}, status=status.HTTP_404_NOT_FOUND)

        resume_file = request.FILES.get('resume')
        Resume.objects.create(applicant=applicant, resume_file=resume_file)

        return Response({"message": "Resume uploaded successfully"}, status=status.HTTP_200_OK)

def calculate_aggregate_score(applicant):
    total_score = sum([
        applicant.skill_analysis_score,
        applicant.social_media_matching_score,
        applicant.proof_of_work_score,
        applicant.project_analysis_score,
        applicant.primary_verification_score,
        applicant.salary_data_score
    ])
    return total_score