# Generated by Django 4.2.6 on 2023-10-29 06:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("questions_app", "0002_applicant_useranswer_resume_answer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="applicant",
            name="proof_of_work_score",
        ),
    ]
