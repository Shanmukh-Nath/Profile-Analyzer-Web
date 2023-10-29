from django.contrib.auth.models import AbstractUser
from django.db import models

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('sales', 'Sales'),
        ('tech', 'Tech'),
    ]
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES)
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    option_1_ps = models.IntegerField()
    option_2_ps = models.IntegerField()
    option_3_ps = models.IntegerField()
    option_4_ps = models.IntegerField()


class IQQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('IQ_sales', 'iq_Sales'),
        ('IQ_tech', 'iq_Tech'),
    ]
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES)
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)




class Applicant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    tech_score = models.PositiveIntegerField(default=0)
    sales_score = models.PositiveIntegerField(default=0)
    overall_score = models.PositiveIntegerField(default=0)
    iq_score = models.PositiveIntegerField(default=0)
    dominant_domain = models.CharField(max_length=5, choices=[('tech', 'Tech'), ('sales', 'Sales')], null=True, blank=True)
    facebook_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    leetcode_link = models.URLField(blank=True, null=True)
    hacker_rank_link = models.URLField(blank=True, null=True)
    # Metrics for Social Profile Analysis (You can modify these as per your analytics results)
    skill_analysis_score = models.PositiveIntegerField(default=0)
    social_media_matching_score = models.PositiveIntegerField(default=0)
    #proof_of_work_score = models.PositiveIntegerField(default=0)
    project_analysis_score = models.PositiveIntegerField(default=0)
    primary_verification_score = models.PositiveIntegerField(default=0)
    salary_data_score = models.PositiveIntegerField(default=0)
    domain_suitability = models.CharField(max_length=10, choices=[('sales', 'Sales'), ('tech', 'Tech')], blank=True,
                                          null=True)


class Resume(models.Model):
    applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/')

class Answer(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    iq_question = models.ForeignKey(IQQuestion,on_delete=models.CASCADE, default=0)
    selected_option = models.IntegerField() # Store the selected option number (1, 2, 3, or 4)
    score = models.IntegerField() # This will be populated based on the choice made


# class Profile(models.Model):
#     user = models.OneToOneField(Applicant, on_delete=models.CASCADE)
#     facebook = models.URLField(blank=True)
#     instagram = models.URLField(blank=True)
#     linkedin = models.URLField(blank=True)
#     github = models.URLField(blank=True)
#     leetcode = models.URLField(blank=True)
#     hacker_rank = models.URLField(blank=True)
#     tech_score = models.IntegerField(default=0)
#     sales_score = models.IntegerField(default=0)
#     iq_score = models.IntegerField(default=0)

class UserAnswer(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.PositiveIntegerField()  # 1, 2, 3, or 4
    points_awarded = models.PositiveIntegerField()

