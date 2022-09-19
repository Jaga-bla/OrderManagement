# Generated by Django 4.1.1 on 2022-09-18 10:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('type', models.CharField(choices=[('PUBLIC_AUCTION', 'Public Auction'), ('QUICK_TENDER', 'Quick Tender')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('catalog_number', models.CharField(default='0000', max_length=100)),
                ('impuls_number', models.CharField(default='0000', max_length=100)),
                ('producent', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.CharField(max_length=100)),
                ('vat', models.CharField(default='%', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_products', models.PositiveIntegerField(default=1)),
                ('contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='layout.contract')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='layout.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('date_of_order', models.DateField(default=django.utils.timezone.now)),
                ('is_ordered', models.BooleanField()),
                ('is_delivered', models.BooleanField()),
                ('contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='layout.contract')),
                ('contractor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='layout.contractor')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='layout.product')),
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
            field=models.ManyToManyField(to='layout.product'),
        ),
    ]
