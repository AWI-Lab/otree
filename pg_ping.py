# -*- coding: utf-8 -*-
import psycopg2

from django.db import connections

connection = psycopg2.connect(
    database=connections['default'].settings_dict['NAME'],
    user=connections['default'].settings_dict['USER'],
    password=connections['default'].settings_dict['PASSWORD'],
    host=connections['default'].settings_dict['HOST'],
    port=connections['default'].settings_dict['PORT']
)
