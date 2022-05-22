# Generated by Django 3.2.9 on 2022-05-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=255)),
                ('money', models.FloatField(default=0.0, max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='money',
            field=models.FloatField(default=0, max_length=15),
        ),
    ]
