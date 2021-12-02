# Generated by Django 3.2.9 on 2021-12-02 08:10

import uuid

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Plot",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("geom", django.contrib.gis.db.models.fields.PolygonField(srid=2056)),
                ("name", models.CharField(max_length=255)),
                ("rotation_sections", models.IntegerField(default=0)),
                ("rotation_treatments", models.IntegerField(default=0)),
                ("planned_next_section", models.DateField(blank=True, null=True)),
                ("planned_next_treatment", models.DateField(blank=True, null=True)),
            ],
            options={
                "verbose_name": " Plot",
            },
        ),
        migrations.CreateModel(
            name="Sector",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "  Sector",
            },
        ),
        migrations.CreateModel(
            name="Treatment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date", models.DateField(blank=True, null=True)),
                ("remarks", models.TextField(blank=True, default="")),
                ("description", models.TextField(blank=True, default="")),
                (
                    "plot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sylvis.plot"
                    ),
                ),
            ],
            options={
                "verbose_name": "Treatment",
            },
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date", models.DateField(blank=True, null=True)),
                ("remarks", models.TextField(blank=True, default="")),
                ("volume", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "plot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sylvis.plot"
                    ),
                ),
            ],
            options={
                "verbose_name": "Section",
            },
        ),
        migrations.AddField(
            model_name="plot",
            name="sector",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="sylvis.sector",
            ),
        ),
        migrations.CreateModel(
            name="Inventory",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date", models.DateField(blank=True, null=True)),
                ("remarks", models.TextField(blank=True, default="")),
                (
                    "standing_volume",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "plot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sylvis.plot"
                    ),
                ),
            ],
            options={
                "verbose_name": "Inventory",
            },
        ),
    ]
