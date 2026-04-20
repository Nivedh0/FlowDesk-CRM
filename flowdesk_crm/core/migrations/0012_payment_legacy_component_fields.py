from decimal import Decimal

from django.db import migrations, models


def add_missing_payment_legacy_columns(apps, schema_editor):
    table_name = 'core_payment'
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        existing_columns = {
            column.name
            for column in connection.introspection.get_table_description(cursor, table_name)
        }

    column_sql = {
        'payment_kind': "ALTER TABLE core_payment ADD COLUMN payment_kind VARCHAR(10) NOT NULL DEFAULT 'course_fee'",
        'advance_component': "ALTER TABLE core_payment ADD COLUMN advance_component DECIMAL(10,2) NOT NULL DEFAULT 0.00",
        'course_fee_component': "ALTER TABLE core_payment ADD COLUMN course_fee_component DECIMAL(10,2) NOT NULL DEFAULT 0.00",
    }

    for column_name, sql in column_sql.items():
        if column_name in existing_columns:
            continue
        schema_editor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_fee_legacy_payment_fields'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(add_missing_payment_legacy_columns, migrations.RunPython.noop),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='payment',
                    name='advance_component',
                    field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
                ),
                migrations.AddField(
                    model_name='payment',
                    name='course_fee_component',
                    field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
                ),
                migrations.AddField(
                    model_name='payment',
                    name='payment_kind',
                    field=models.CharField(
                        choices=[('advance', 'Advance'), ('course_fee', 'Course Fee'), ('mixed', 'Mixed')],
                        default='course_fee',
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]
