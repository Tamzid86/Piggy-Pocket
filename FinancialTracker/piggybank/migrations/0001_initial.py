# Generated by Django 5.1.4 on 2024-12-15 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField()),
                ('last_name', models.CharField()),
                ('address', models.CharField()),
                ('bio', models.CharField()),
            ],
        ),
    ]
