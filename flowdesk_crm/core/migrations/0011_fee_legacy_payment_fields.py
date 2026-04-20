from decimal import Decimal

from django.db import migrations, models


def add_missing_fee_legacy_columns(apps, schema_editor):
    table_name = 'core_fee'
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        existing_columns = {
            column.name
            for column in connection.introspection.get_table_description(cursor, table_name)
        }

    column_sql = {
        'advance_paid': "ALTER TABLE core_fee ADD COLUMN advance_paid DECIMAL(10,2) NOT NULL DEFAULT 0.00",
        'course_fee_paid': "ALTER TABLE core_fee ADD COLUMN course_fee_paid DECIMAL(10,2) NOT NULL DEFAULT 0.00",
        'remaining_balance': "ALTER TABLE core_fee ADD COLUMN remaining_balance DECIMAL(10,2) NOT NULL DEFAULT 0.00",
        'advance_amount': "ALTER TABLE core_fee ADD COLUMN advance_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00",
    }

    for column_name, sql in column_sql.items():
        if column_name in existing_columns:
            continue
        schema_editor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_sessionupdate_assignment_marks'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(add_missing_fee_legacy_columns, migrations.RunPython.noop),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='fee',
                    name='advance_amount',
                    field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
                ),
                migrations.AddField(
                    model_name='fee',
                    name='advance_paid',
                    field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
                ),
                migrations.AddField(
                    model_name='fee',
                    name='course_fee_paid',
                    field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
                ),
                migrations.AddField(
                    model_name='fee',
                    name='remaining_balance',
                    field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
                ),
            ],
        ),
    ]
