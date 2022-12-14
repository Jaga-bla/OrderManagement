# Generated by Django 4.1.4 on 2023-01-06 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(default='0000', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('type', models.CharField(choices=[('PUBLIC_AUCTION', 'Public Auction'), ('QUICK_TENDER', 'Quick Tender')], max_length=100)),
                ('email_sent', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('catalog_number', models.CharField(default='0000', max_length=100)),
                ('impuls_number', models.CharField(default='0000', max_length=100)),
                ('producer', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.CharField(max_length=100)),
                ('vat', models.CharField(default='%', max_length=100)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuantifiedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_product', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='layout.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='layout.contract')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='layout.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_order', models.DateField(default=django.utils.timezone.now)),
                ('is_ordered', models.BooleanField(default=False, verbose_name='Is ordered')),
                ('is_delivered', models.BooleanField(default=False, verbose_name='Is Ordered')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='layout.contract')),
                ('ordered_products', models.ManyToManyField(to='layout.orderproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='contractor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='layout.contractor'),
        ),
        migrations.AddField(
            model_name='contract',
            name='products',
            field=models.ManyToManyField(to='layout.quantifiedproduct'),
        ),
        migrations.AddField(
            model_name='contract',
            name='user_responsible',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_reponsible', to=settings.AUTH_USER_MODEL),
        ),
    ]
