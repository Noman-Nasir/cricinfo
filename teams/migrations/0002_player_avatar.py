# Generated by Django 3.2.6 on 2021-11-15 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='avatar',
            field=models.ImageField(default='shaheen.jpeg', upload_to=''),
            preserve_default=False,
        ),
    ]