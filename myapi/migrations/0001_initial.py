# Generated by Django 3.0.8 on 2020-08-17 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('publishers', models.CharField(max_length=60)),
                ('year_published', models.IntegerField()),
                ('max_players', models.IntegerField()),
                ('image_url', models.ImageField(upload_to='static/images')),
                ('msrp', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
