# Generated by Django 2.2.9 on 2020-02-15 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rule_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='rules',
            field=models.ManyToManyField(to='main.Rule'),
        ),
    ]
