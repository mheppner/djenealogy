# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('xref', models.CharField(max_length=15)),
                ('tag', models.CharField(max_length=127)),
                ('value', models.CharField(max_length=255, null=True, blank=True)),
                ('level', models.IntegerField()),
            ],
            options={
                'ordering': ('husband__surname', 'husband__given_name', 'wife__surname', 'wife__given_name'),
                'verbose_name_plural': 'families',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FamilyEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(max_length=255, null=True, blank=True)),
                ('level', models.IntegerField()),
                ('place', models.CharField(max_length=255, null=True, blank=True)),
                ('date', models.CharField(max_length=32, null=True, blank=True)),
                ('type', models.CharField(default=(b'EVEN', b'General event'), max_length=7, choices=[(b'EVEN', b'General event'), (b'ANUL', b'Annulment'), (b'CENS', b'Census'), (b'DIV', b'Divorce'), (b'DIVF', b'Divorce filed'), (b'ENGA', b'Engagement'), (b'MARR', b'Marriage'), (b'MARB', b'Marriage bann'), (b'MARC', b'Marriage contract'), (b'MARL', b'Marriage license'), (b'MARS', b'Marriage settlement')])),
                ('family', models.ForeignKey(related_name='events', to='djenealogy.Family')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gedcom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=b'gedcoms')),
                ('name', models.CharField(max_length=127)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('xref', models.CharField(max_length=15)),
                ('tag', models.CharField(max_length=127)),
                ('value', models.CharField(max_length=255, null=True, blank=True)),
                ('level', models.IntegerField()),
                ('sex', models.CharField(default=(b'U', b'Unknown'), max_length=1, choices=[(b'U', b'Unknown'), (b'M', b'Male'), (b'F', b'Female')])),
                ('relate1', models.PositiveIntegerField(null=True, blank=True)),
                ('relate2', models.PositiveIntegerField(null=True, blank=True)),
                ('surname', models.CharField(max_length=127, blank=True)),
                ('given_name', models.CharField(max_length=127, blank=True)),
                ('prefix', models.CharField(max_length=127, blank=True)),
                ('suffix', models.CharField(max_length=127, blank=True)),
                ('nickname', models.CharField(max_length=127, blank=True)),
                ('birth_year', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('death_year', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('gedcom', models.ForeignKey(to='djenealogy.Gedcom')),
            ],
            options={
                'ordering': ('surname', 'given_name', 'nickname'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IndividualEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(max_length=255, null=True, blank=True)),
                ('level', models.IntegerField()),
                ('place', models.CharField(max_length=255, null=True, blank=True)),
                ('date', models.CharField(max_length=32, null=True, blank=True)),
                ('type', models.CharField(default=(b'EVEN', b'General event'), max_length=7, choices=[(b'EVEN', b'General event'), (b'BIRT', b'Birth'), (b'CHR', b'Christening'), (b'DEAT', b'Death'), (b'BURI', b'Burial'), (b'CREM', b'Cremation'), (b'ADOP', b'Adoption'), (b'BAPM', b'Baptism'), (b'BARM', b'Bar Mitzvah'), (b'BASM', b'Bas Mitzvah'), (b'BLES', b'Blessing'), (b'CHRA', b'Adult christening'), (b'CONF', b'Confirmation'), (b'FCOM', b'First communion'), (b'ORDN', b'Ordination'), (b'NATU', b'Naturalization'), (b'EMIG', b'Emigration'), (b'IMMI', b'Immigration'), (b'CENS', b'Census'), (b'PROB', b'Property'), (b'WILL', b'Will'), (b'GRAD', b'Graduation'), (b'RETI', b'Retirement')])),
                ('gedcom', models.ForeignKey(to='djenealogy.Gedcom')),
                ('individual', models.ForeignKey(related_name='events', to='djenealogy.Individual')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('xref', models.CharField(max_length=15)),
                ('tag', models.CharField(max_length=127)),
                ('value', models.CharField(max_length=255, null=True, blank=True)),
                ('level', models.IntegerField()),
                ('full_text', models.TextField(blank=True)),
                ('gedcom', models.ForeignKey(to='djenealogy.Gedcom')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='individualevent',
            name='notes',
            field=models.ManyToManyField(to='djenealogy.Note', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='individual',
            name='notes',
            field=models.ManyToManyField(to='djenealogy.Note', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='individual',
            unique_together=set([('gedcom', 'xref')]),
        ),
        migrations.AddField(
            model_name='familyevent',
            name='gedcom',
            field=models.ForeignKey(to='djenealogy.Gedcom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='familyevent',
            name='notes',
            field=models.ManyToManyField(to='djenealogy.Note', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='children',
            field=models.ManyToManyField(related_name='parents', null=True, to='djenealogy.Individual', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='gedcom',
            field=models.ForeignKey(to='djenealogy.Gedcom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='husband',
            field=models.ForeignKey(related_name='husband_roles', blank=True, to='djenealogy.Individual', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='notes',
            field=models.ManyToManyField(to='djenealogy.Note', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='family',
            name='wife',
            field=models.ForeignKey(related_name='wife_roles', blank=True, to='djenealogy.Individual', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='family',
            unique_together=set([('gedcom', 'xref', 'husband', 'wife')]),
        ),
    ]
