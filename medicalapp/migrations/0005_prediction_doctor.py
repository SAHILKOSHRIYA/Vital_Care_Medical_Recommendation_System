# Generated by Django 4.1.7 on 2024-01-20 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicalapp', '0004_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medicalapp.doctor'),
        ),
    ]
