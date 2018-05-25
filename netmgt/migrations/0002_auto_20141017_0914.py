# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netmgt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('name', models.CharField(max_length=250, unique=True, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TemplateRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, blank=True)),
                ('ttl', models.IntegerField(null=True, verbose_name=b'TTL', blank=True)),
                ('type', models.CharField(max_length=8, choices=[(b'A', b'A'), (b'AAAA', b'AAAA'), (b'CERT', b'CERT'), (b'CNAME', b'CNAME'), (b'DNSKEY', b'DNSKEY'), (b'DS', b'DS'), (b'DNSKEY', b'DNSKEY'), (b'KEY', b'KEY'), (b'LOC', b'LOC'), (b'MX', b'MX'), (b'NAPTR', b'NAPTR'), (b'NS', b'NS'), (b'NSEC', b'NSEC'), (b'PTR', b'PTR'), (b'RRSIG', b'RRSIG'), (b'SPF', b'SPF'), (b'SRV', b'SRV'), (b'TXT', b'TXT')])),
                ('value', models.CharField(max_length=250)),
                ('template', models.ForeignKey(to='netmgt.Template', on_delete = models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Record',
            new_name='ZoneRecord',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='id',
        ),
        migrations.RemoveField(
            model_name='devicetype',
            name='id',
        ),
        migrations.RemoveField(
            model_name='operatingsystem',
            name='id',
        ),
        migrations.AddField(
            model_name='zone',
            name='templates',
            field=models.ManyToManyField(to='netmgt.Template'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='nick',
            field=models.CharField(max_length=250, unique=True, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='devicetype',
            name='name',
            field=models.CharField(max_length=250, unique=True, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='operatingsystem',
            name='name',
            field=models.CharField(max_length=250, unique=True, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='zone',
            name='name',
            field=models.CharField(max_length=250, unique=True, serialize=False, primary_key=True),
        ),
    ]
