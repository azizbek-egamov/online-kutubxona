# Generated by Django 5.0.6 on 2024-07-06 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_shortner'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=50)),
            ],
        ),
    ]
