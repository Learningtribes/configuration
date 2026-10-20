sed -i '29a import MySQLdb._mysql\
sys.modules.setdefault("_mysql", MySQLdb._mysql)' /edx/app/edxapp/edx-platform/manage.py