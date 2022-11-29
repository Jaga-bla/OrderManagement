# Generated by Django 4.1.3 on 2022-11-27 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('layout', '0004_contract_ending'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='ending',
        ),
        migrations.AlterField(
            model_name='contract',
            name='user_responsible',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]