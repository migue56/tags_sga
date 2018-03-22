# Generated by Django 2.0.3 on 2018-03-21 22:57

from django.db import migrations, models


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
                ('SGAIndicator', models.ManyToManyField(to='tags_sga.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Pictogram',
            fields=[
                ('codename', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('ilustrator_oit', models.FileField(blank=True, null=True, upload_to='pictograms/')),
                ('ilustrator_sga', models.FileField(blank=True, null=True, upload_to='pictograms/')),
                ('warning_level', models.IntegerField()),
                ('human_tag', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Prudence',
            fields=[
                ('codename', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('general_help', models.TextField()),
                ('conditions_use', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SGAIndicator',
            fields=[
                ('codename', models.CharField(max_length=150, primary_key=True, serialize=False)),
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
            ],
        ),
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physical_warnig', models.TextField()),
                ('health_safe', models.TextField()),
            ],
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
