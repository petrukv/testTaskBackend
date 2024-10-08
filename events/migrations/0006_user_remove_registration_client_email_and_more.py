# Generated by Django 5.1.1 on 2024-09-29 22:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0005_alter_registration_manage_code"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("username", models.CharField(max_length=150, unique=True)),
                ("password", models.CharField(max_length=128)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="registration",
            name="client_email",
        ),
        migrations.AddField(
            model_name="registration",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="registrations",
                to="events.user",
            ),
            preserve_default=False,
        ),
    ]
