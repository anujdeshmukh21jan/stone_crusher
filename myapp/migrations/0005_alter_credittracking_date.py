# Generated by Django 4.2.16 on 2024-10-21 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_debittracking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credittracking',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]