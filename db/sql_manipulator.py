# coding: utf-8
import MySQLdb
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
print(sys.getdefaultencoding())
class SQLManipulator():
    def __init__(self, ):
        i=0

    def sql_manipulator(self, msg):
        connection = MySQLdb.connect(
            host='localhost',
            user='noza',
            passwd='Pass_123',
            db='horse',
            use_unicode=True,
            charset='utf8')
        cursor = connection.cursor()

        cursor.execute(msg)
        retval = cursor.fetchall()
        connection.commit()
        connection.close()

        return retval
