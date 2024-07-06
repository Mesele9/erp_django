# common_user/db_backup_restore.py
import os
from django.conf import settings

def get_database_info():
    db_settings = settings.DATABASES['default']
    db_type = db_settings['ENGINE'].split('.')[-1]
    db_name = db_settings['NAME']
    db_user = db_settings.get('USER', '')
    db_password = db_settings.get('PASSWORD', '')
    return db_type, db_name, db_user, db_password

def backup_database(backup_path):
    db_type, db_name, db_user, db_password = get_database_info()
    if db_type == 'sqlite3':
        # SQLite backup
        os.system(f'python manage.py dumpdata > {backup_path}')
    elif db_type == 'mysql':
        # MySQL backup
        os.system(f'mysqldump -u {db_user} -p{db_password} {db_name} > {backup_path}')
    elif db_type == 'postgresql':
        # PostgreSQL backup
        os.environ['PGPASSWORD'] = db_password
        os.system(f'pg_dump -U {db_user} -F c {db_name} > {backup_path}')
    else:
        raise ValueError(f'Unsupported database type: {db_type}')

def restore_database(backup_path):
    db_type, db_name, db_user, db_password = get_database_info()
    if db_type == 'sqlite3':
        # SQLite restore
        os.system(f'python manage.py loaddata {backup_path}')
    elif db_type == 'mysql':
        # MySQL restore
        os.system(f'mysql -u {db_user} -p{db_password} {db_name} < {backup_path}')
    elif db_type == 'postgresql':
        # PostgreSQL restore
        os.environ['PGPASSWORD'] = db_password
        os.system(f'psql -U {db_user} -d {db_name} -f {backup_path}')
    else:
        raise ValueError(f'Unsupported database type: {db_type}')
