# Generated by Django 5.1.2 on 2024-10-18 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InfoProduct',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('tig_id', models.CharField(blank=True, default='', max_length=20)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('category', models.IntegerField(default=-1)),
                ('price', models.FloatField(default=0.0)),
                ('unit', models.CharField(blank=True, default='', max_length=20)),
                ('availability', models.BooleanField(default=True)),
                ('sale', models.BooleanField(default=False)),
                ('discount', models.FloatField(default=0.0)),
                ('comments', models.CharField(blank=True, default='', max_length=100)),
                ('owner', models.CharField(blank=True, default='tig_orig', max_length=20)),
                ('quantityInStock', models.IntegerField(default='0')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_purchase', models.BooleanField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monTiGMagasin.infoproduct')),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
    ]
