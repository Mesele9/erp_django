import os
from django.conf import settings
from django.utils.timezone import now

def get_db_info():
    db_settings = settings.DATABASES['default']
    db_name = db_settings['NAME']
    db_user = db_settings['USER']
    db_password = db_settings['PASSWORD']
    db_engine = db_settings['ENGINE']

    if 'mysql' in db_engine:
        db_type = 'mysql'
    elif 'postgresql' in db_engine:
        db_type = 'postgresql'
    else:
        db_type = 'sqlite'

    return db_type, db_name, db_user, db_password

def backup_database(backup_path):
    db_type, db_name, db_user, db_password = get_db_info()
    timestamp = now().strftime('%Y%m%d%H%M%S')
    backup_filename = f'db_backup_{timestamp}.sql'
    full_backup_path = os.path.join(backup_path, backup_filename)

    if db_type == 'mysql':
        os.system(f'mysqldump -u {db_user} -p{db_password} {db_name} > {full_backup_path}')
    elif db_type == 'postgresql':
        os.environ['PGPASSWORD'] = db_password
        os.system(f'pg_dump -U {db_user} -F c {db_name} > {full_backup_path}')
    else:
        os.system(f'python manage.py dumpdata > {full_backup_path}')

    return full_backup_path

def restore_database(backup_file):
    db_type, db_name, db_user, db_password = get_db_info()
    backup_path = f'/tmp/{backup_file.name}'
    with open(backup_path, 'wb') as f:
        for chunk in backup_file.chunks():
            f.write(chunk)

    if db_type == 'mysql':
        os.system(f'mysql -u {db_user} -p{db_password} {db_name} < {backup_path}')
    elif db_type == 'postgresql':
        os.environ['PGPASSWORD'] = db_password
        os.system(f'pg_restore -U {db_user} -d {db_name} -c {backup_path}')
    else:
        os.system(f'python manage.py loaddata {backup_path}')
