# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField()),
                ('prefix_len', models.IntegerField(verbose_name=b'Prefix Length')),
                ('name', models.CharField(max_length=250)),
                ('reverse_zone', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('info', models.CharField(max_length=250, blank=True)),
                ('contact', models.ForeignKey(to='netmgt.Contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, blank=True)),
                ('ttl', models.IntegerField(null=True, verbose_name=b'TTL', blank=True)),
                ('type', models.CharField(max_length=8, choices=[(b'A', b'A'), (b'AAAA', b'AAAA'), (b'CERT', b'CERT'), (b'CNAME', b'CNAME'), (b'DNSKEY', b'DNSKEY'), (b'DS', b'DS'), (b'DNSKEY', b'DNSKEY'), (b'KEY', b'KEY'), (b'LOC', b'LOC'), (b'MX', b'MX'), (b'NAPTR', b'NAPTR'), (b'NS', b'NS'), (b'NSEC', b'NSEC'), (b'PTR', b'PTR'), (b'RRSIG', b'RRSIG'), (b'SPF', b'SPF'), (b'SRV', b'SRV'), (b'TXT', b'TXT')])),
                ('value', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('name', models.CharField(max_length=250, serialize=False, primary_key=True)),
                ('ttl', models.IntegerField(null=True, verbose_name=b'TTL', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='record',
            name='zone',
            field=models.ForeignKey(to='netmgt.Zone'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='device',
            name='os',
            field=models.ForeignKey(verbose_name=b'Operating System', to='netmgt.OperatingSystem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='device',
            name='type',
            field=models.ForeignKey(to='netmgt.DeviceType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='device',
            field=models.ForeignKey(to='netmgt.Device'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='zone',
            field=models.ForeignKey(to='netmgt.Zone'),
            preserve_default=True,
        ),
    ]
