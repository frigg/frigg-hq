from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0020_project_can_deploy'),
    ]

    operations = [
        migrations.CreateModel(
            name='PRDeployment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False,
                                        auto_created=True)),
                ('port', models.IntegerField()),
                ('image', models.CharField(max_length=255)),
                ('log', models.TextField(blank=True)),
                ('succeeded', models.NullBooleanField()),
                ('build', models.OneToOneField(to='builds.Build', related_name='deployment')),
            ],
            options={
                'verbose_name_plural': 'Pull request deployments',
                'verbose_name': 'Pull request deployment',
            },
        ),
    ]
