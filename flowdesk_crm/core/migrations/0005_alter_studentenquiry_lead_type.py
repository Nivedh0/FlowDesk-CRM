from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_studentenquiry_lead_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentenquiry',
            name='lead_type',
            field=models.CharField(
                choices=[
                    ('new', 'New'),
                    ('dnp', 'DNP'),
                    ('hot', 'Hot'),
                    ('warm', 'Warm'),
                    ('cold', 'Cold'),
                    ('done', 'Done'),
                ],
                default='new',
                max_length=10,
            ),
        ),
    ]
