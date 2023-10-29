from django.urls import path
from .views import RandomQuestionList, SaveAnswer, ApplicantProfile, SubmitSocials, UploadResume
from . import views

urlpatterns = [
    path('random_questions/', RandomQuestionList.as_view(), name='random_questions'),
    path('applicant_profile/', ApplicantProfile.as_view(), name='applicant_profile'),
    path('save_answer/', SaveAnswer.as_view(), name='save_answer'),
    path('submit_socials/', SubmitSocials.as_view(), name='submit_answers'),
    path('upload_resume/', UploadResume.as_view(), name='upload_resume'),
]
