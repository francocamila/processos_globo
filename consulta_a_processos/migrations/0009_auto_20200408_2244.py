# Generated by Django 2.2.12 on 2020-04-09 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta_a_processos', '0008_auto_20200408_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processos',
            name='incidente_id',
            field=models.TextField(blank=True, default='id'),
        ),
    ]