# Generated by Django 3.2.9 on 2021-12-02 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sylvis", "0008_auto_20211202_1642"),
    ]

    operations = [
        migrations.CreateModel(
            name="DummyMapModel",
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
            ],
            options={
                "verbose_name_plural": "Main map",
                "managed": False,
            },
        ),
    ]
