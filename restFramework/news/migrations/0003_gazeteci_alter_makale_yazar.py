# Generated by Django 5.0.7 on 2024-07-23 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_makale_guncellenme_tarihi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gazeteci',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=120)),
                ('soy_isim', models.CharField(max_length=120)),
                ('biyografi', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='makale',
            name='yazar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Makaleler', to='news.gazeteci'),
        ),
    ]
