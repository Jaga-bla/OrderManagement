# Generated by Django 4.1.3 on 2022-12-03 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layout', '0006_company_contract_author_contractor_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='author',
        ),
        migrations.AddField(
            model_name='company',
            name='password',
            field=models.CharField(default='0000', max_length=100),
        ),
    ]