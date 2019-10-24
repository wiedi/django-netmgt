# Generated by Django 2.0.5 on 2018-05-25 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netmgt', '0005_auto_20170509_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='os',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='netmgt.OperatingSystem', verbose_name='Operating System'),
        ),
    ]