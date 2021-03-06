# Generated by Django 3.1.7 on 2021-04-14 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LargeCap',
            fields=[
                ('name', models.TextField(blank=True, primary_key=True, serialize=False)),
                ('prod_rate', models.FloatField(blank=True, null=True)),
                ('debt_rate', models.FloatField(blank=True, null=True)),
                ('cred_rate', models.FloatField(blank=True, null=True)),
                ('liq_rate', models.FloatField(blank=True, null=True)),
                ('grow_rate', models.FloatField(blank=True, null=True)),
                ('oper_rate', models.FloatField(blank=True, null=True)),
                ('sent_rate', models.FloatField(blank=True, null=True)),
                ('vol_strength', models.FloatField(blank=True, null=True)),
                ('nd_vol_prob', models.FloatField(blank=True, null=True)),
                ('nw_vol_prob', models.FloatField(blank=True, null=True)),
                ('pa_prob', models.FloatField(blank=True, null=True)),
                ('bull_rev_prob', models.FloatField(blank=True, null=True)),
                ('bear_rev_prob', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Large_Cap',
                'managed': False,
            },
        ),
    ]
