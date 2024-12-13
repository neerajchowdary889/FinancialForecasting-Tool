# Generated by Django 5.1.2 on 2024-12-12 16:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FinancialData",
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
                ("date", models.DateField()),
                ("revenue", models.DecimalField(decimal_places=2, max_digits=12)),
                ("expenses", models.DecimalField(decimal_places=2, max_digits=12)),
                ("profit", models.DecimalField(decimal_places=2, max_digits=12)),
                ("category", models.CharField(max_length=100)),
                ("notes", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="Forecast",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("forecast_date", models.DateField()),
                (
                    "predicted_revenue",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                (
                    "predicted_expenses",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                (
                    "predicted_profit",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                (
                    "confidence_level",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-forecast_date"],
            },
        ),
    ]