import os
import time
from MyTools import *

# while True:
#    if time.strftime('%H:%M') == '10:58':
print 'Begin with %s' % time.strftime('%Y-%m-%d %H:%M')
flist = searchFile(os.getcwd(), '.zip')
for file in flist:
    removeFile(os.getcwd() + os.sep + 'SQLs')
    sql_list = unzipFile(file, 'SQLs', 'hangar')
    removeFile(os.getcwd() + os.sep + 'Datas')
    if sql_list:
        for f_sql in sql_list:
            sql = readFile(f_sql)
            print ''
            conn = connectOracle('pharmacy', 'pharmacy', 'his')
            print 'Picking %s...' % getFilename(f_sql)
            print 'Pick data %s rows' % str(pickData(conn, sql, getFilename(f_sql)))
            print 'Pick %s successed!' % getFilename(f_sql)
    print ''
    zipFile(searchFile(os.getcwd() + os.sep + 'Datas', '.txt'), file, 'hangar')
    removeFile(os.getcwd() + os.sep + 'Datas')
    removeFile(os.getcwd() + os.sep + 'SQLs')
    print ''
print 'Complete with %s' % time.strftime('%Y-%m-%d %H:%M')
