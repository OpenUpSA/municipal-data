from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        # NOTE: The previous migration probably looks different for you, so
        # modify this.
        ('infrastructure', '0008_auto_20200109_1848'),
    ]

    migration = '''
        CREATE TRIGGER content_search_update BEFORE INSERT OR UPDATE
        ON infrastructure_project FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(
            content_search, 'pg_catalog.english',
            function, project_description, project_number, project_type,
            mtsf_service_outcome, iudf, own_strategic_objectives, asset_class, asset_subclass
         );

        -- Force triggers to run and populate the text_search column.
        UPDATE infrastructure_project set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER content_search ON infrastructure_project;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]

