import csv
import os
import sqlite3

from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR

PATH_DIR = os.path.join(BASE_DIR, 'static/data')

PATH_TO_BD = '../api_yamdb/db.sqlite3'

CONFORMITY = {
    'users': 'reviews_user',
    'category': 'reviews_category',
    'genre': 'reviews_genre',
    'titles': 'reviews_title',
    'genre_title': 'reviews_titlegenre',
    'review': 'reviews_review',
    'comments': 'reviews_comment',
}


class Command(BaseCommand):
    help = 'Data import...........'

    def handle(self, *args, **options):
        con = sqlite3.connect(PATH_TO_BD)
        cur = con.cursor()

        for file in os.listdir(PATH_DIR):
            path_to_file = os.path.join(PATH_DIR, file)
            table_name = CONFORMITY[
                os.path.splitext(os.path.basename(file))[0]
            ]

            with open(path_to_file, 'r', encoding='utf-8') as f_open_csv:
                rows = csv.DictReader(f_open_csv)

                for row in rows:
                    columns = ', '.join(row.keys())
                    placeholders = ', '.join('?' * len(row))
                    sql = 'INSERT INTO {} ({}) VALUES ({})'.format(
                        table_name, columns, placeholders
                    )
                    values = [
                        int(x) if x.isnumeric() else x for x in row.values()
                    ]
                    cur.execute(sql, values)

        con.commit()
        con.close()
        print()
        print()
        print('The data from .csv-files are imported.')
        print('======================================')
        print()

# Чтобы скрипт работал пришлось видоизменить CSV файлы
# users добавил is_superuser,is_staff,is_active,date_joined и confirmation_code
# также необходимо добавить по 1 запятой для каждого столбца
# Для confirmation_code из-за уникальности параметра
# добавлены указаны реальные значения
# Командна - python manage.py unpackingcsv
