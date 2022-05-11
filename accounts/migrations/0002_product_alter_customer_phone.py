# Generated by Django 4.0.4 on 2022-05-11 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, null=True)),
                ('price', models.FloatField(null=True)),
                ('catageory', models.CharField(max_length=25, null=True)),
                ('description', models.CharField(max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
