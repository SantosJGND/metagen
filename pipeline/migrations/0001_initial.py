# Generated by Django 4.0.2 on 2022-03-08 13:44

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('samples', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='files/fofn'), upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='module', to='pipeline.module')),
                ('tech', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tech', to='pipeline.technology')),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.CharField(max_length=20)),
                ('results', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='files/projects'), upload_to='')),
                ('args', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='files/projects'), upload_to='')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pipeline.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ASSEMBLY', models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, related_name='assembly', to='pipeline.software')),
                ('CLASSA', models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, related_name='classa', to='pipeline.software')),
                ('CLASSM', models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, related_name='classm', to='pipeline.software')),
                ('HD', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='hd', to='pipeline.software')),
                ('QC', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qc', to='pipeline.software')),
                ('REMAP', models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, related_name='remap', to='pipeline.software')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pipeline.project')),
                ('tech', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pipeline.technology')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='technology',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pipeline.technology'),
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
