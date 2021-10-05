import  pymysql.cursors

connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='sql_intro'
                                 )
def connect():
    cursor = connection.cursor()
    return cursor

def commit():
    connection.commit()