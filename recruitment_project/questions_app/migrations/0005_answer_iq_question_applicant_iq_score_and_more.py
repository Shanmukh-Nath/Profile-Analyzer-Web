# Generated by Django 4.2.6 on 2023-10-29 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("questions_app", "0004_iqquestion"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="iq_question",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="questions_app.iqquestion",
            ),
        ),
        migrations.AddField(
            model_name="applicant",
            name="iq_score",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="applicant",
            name="overall_score",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
