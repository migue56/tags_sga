# Generated by Django 2.0.3 on 2018-03-23 15:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codename', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marketing_name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Pictogram',
            fields=[
                ('codename', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('ilustrator_sga', models.FileField(blank=True, null=True, upload_to='static/pictograms/')),
                ('ilustrator_oit', models.FileField(blank=True, null=True, upload_to='static/pictograms/')),
                ('warning_level', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(0)])),
                ('human_tag', models.IntegerField(choices=[(5, 'Danger'), (1, 'Attention')], db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Prudence',
            fields=[
                ('codename', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('general_help', models.TextField()),
                ('conditions_use', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SGAIndicator',
            fields=[
                ('codename', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('warning_indication', models.CharField(max_length=255)),
                ('warning_categories', models.ManyToManyField(to='tags_sga.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Sustance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marketing_name', models.CharField(max_length=250)),
                ('cas_number', models.CharField(max_length=150)),
                ('componets', models.ManyToManyField(to='tags_sga.Component')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags_sga.Provider')),
            ],
        ),
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physical_warnig', models.TextField()),
                ('combinations', models.ManyToManyField(blank=True, related_name='_tip_combinations_+', to='tags_sga.Tip')),
            ],
        ),
        migrations.AddField(
            model_name='component',
            name='SGAIndicator',
            field=models.ManyToManyField(to='tags_sga.SGAIndicator'),
        ),
        migrations.AddField(
            model_name='category',
            name='pictogram',
            field=models.ManyToManyField(to='tags_sga.Pictogram'),
        ),
        migrations.AddField(
            model_name='category',
            name='prudence',
            field=models.ManyToManyField(to='tags_sga.Prudence'),
        ),
        migrations.AddField(
            model_name='category',
            name='tips',
            field=models.ManyToManyField(to='tags_sga.Tip'),
        ),
        migrations.AddField(
            model_name='category',
            name='warning_class',
            field=models.ManyToManyField(blank=True, related_name='_category_warning_class_+', to='tags_sga.Category'),
        ),
    ]
