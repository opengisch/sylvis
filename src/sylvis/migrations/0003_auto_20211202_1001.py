# Generated by Django 3.2.9 on 2021-12-02 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sylvis", "0002_auto_20211202_0933"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventory",
            name="remarks",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="section",
            name="remarks",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="treatment",
            name="remarks",
            field=models.TextField(blank=True, null=True),
        ),
    ]
