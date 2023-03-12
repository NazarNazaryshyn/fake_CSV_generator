# Generated by Django 4.1.7 on 2023-03-11 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_schemas', '0002_alter_schemacolumn_data_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_schemas.schema')),
            ],
        ),
    ]
