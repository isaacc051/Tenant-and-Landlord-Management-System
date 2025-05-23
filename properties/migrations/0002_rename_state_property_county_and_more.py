# Generated by Django 4.2.7 on 2025-04-24 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='state',
            new_name='county',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='zipcode',
            new_name='postcode',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='city',
            new_name='town_city',
        ),
        migrations.RemoveField(
            model_name='property',
            name='square_feet',
        ),
        migrations.RemoveField(
            model_name='propertyapplication',
            name='credit_score',
        ),
        migrations.AddField(
            model_name='property',
            name='square_meters',
            field=models.PositiveIntegerField(default=70, help_text='Property size in square meters'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='propertyapplication',
            name='credit_check_consent',
            field=models.BooleanField(default=False, help_text='Consent to perform credit check'),
        ),
        migrations.AddField(
            model_name='propertyapplication',
            name='employment_status',
            field=models.CharField(blank=True, help_text='Current employment status', max_length=50),
        ),
        migrations.AlterField(
            model_name='property',
            name='monthly_rent',
            field=models.DecimalField(decimal_places=2, help_text='Monthly rent in £', max_digits=10),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(choices=[('flat', 'Flat'), ('house', 'House'), ('terraced', 'Terraced House'), ('semi_detached', 'Semi-Detached House'), ('detached', 'Detached House'), ('bungalow', 'Bungalow'), ('cottage', 'Cottage'), ('studio', 'Studio'), ('maisonette', 'Maisonette'), ('commercial', 'Commercial')], max_length=20),
        ),
        migrations.AlterField(
            model_name='propertyapplication',
            name='income',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Monthly income in £', max_digits=10, null=True),
        ),
    ]
