# Generated by Django 2.2.7 on 2021-08-29 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0003_auto_20210828_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancereport',
            name='student_id',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='student_att', to='auths.Students'),
        ),
    ]