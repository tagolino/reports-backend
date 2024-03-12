# Generated by Django 4.2.10 on 2024-03-12 10:05

from django.db import migrations, models
import django.db.models.deletion


def add_template_types_and_sub_types(apps, schema_editor):
    TemplateType = apps.get_model("templates", "TemplateType")
    TemplateSubType = apps.get_model("templates", "TemplateSubType")

    TemplateType.objects.bulk_create([
        TemplateType(name="PROPOSAL"),
        TemplateType(name="INVOICE"),
    ])

    TemplateSubType.objects.bulk_create([
        TemplateSubType(name="HH"),
        TemplateSubType(name="NHH"),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0002_alter_templatedatamapping_mapping_expression'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateSubType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TemplateType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='template',
            name='sub_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='templates.templatesubtype'),
        ),
        migrations.RemoveField(
            model_name='template',
            name='type',
        ),
        migrations.AddField(
            model_name='template',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='templates.templatetype'),
        ),
        migrations.RunPython(add_template_types_and_sub_types),
    ]
