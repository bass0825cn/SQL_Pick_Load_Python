#-*- coding:utf-8 -*-
import os
import sys
import zipfile
import zlib
import shutil
import cx_Oracle
import re
import time


def zipFile(file_list, zip_filename, password):
    '''
    zip the file list into file of zip by password
    '''
    save_zip_filename = getSaveFileName(
        getFilename(zip_filename), 0, 'Outputs')[0]
    print save_zip_filename
    fz = zipfile.ZipFile(save_zip_filename, 'w', zipfile.ZIP_DEFLATED, True)
    fz.setpassword(password)
    for file in file_list:
        dest_file = getFilename(file)
        print 'zip %s...' % dest_file
        fz.write(file, dest_file)
    fz.close()
    print 'zip successed!'


def unzipFile(filename, path, password):
    '''
    unzip the file of zip save to path by password
    '''
    removeFile(os.getcwd() + os.sep + path)
    if path[len(path) - 1] != os.sep:
        path += os.sep
    if zipfile.is_zipfile(filename):
        file_list = []
        fz = zipfile.ZipFile(filename, 'r')
        for file in fz.namelist():
            fz.extract(file, path, password)
            file_list.append(os.getcwd() + os.sep + path + file)
        fz.close()
        return file_list
    else:
        return None


def removeFile(path):
    '''
    delete files from path
    '''
    fl = os.listdir(path)
    for f in fl:
        fp = os.path.join(path, f)
        if os.path.isfile(fp):
            os.remove(fp)
        elif os.path.isdir(fp):
            shutil.rmtree(fp, True)


def searchFile(path, word, contain_dir=False):
    '''
    Get File List
    '''
    file_list = []
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp) and word in filename:
            file_list.append(fp)
        elif os.path.isdir(fp):
            if contain_dir:
                file_list.append(searchFile(fp, word, containDir))
    return file_list


def readFile(filename):
    '''
    read string from file
    '''
    file_object = open(filename, 'r')
    file_text = ''
    try:
        file_text = file_object.read()
    finally:
        file_object.close()
    return file_text


def connectOracle(username, password, tnsname):
    '''
    connect oracle
    return connection
    '''
    try:
        conn = cx_Oracle.connect(username, password, tnsname)
        print 'Connect Success!'
    except Exception, e:
        print e
    return cx_Oracle.connect(username, password, tnsname)


def replaceString(source):
    '''
    replace '\r\n','\r','\n' from string
    replace ',' to '，' from string
    '''
    source = source.replace('\r\n', '')
    source = source.replace('\r', '')
    source = source.replace('\n', '')
    source = source.replace(',', '，')
    return source


def saveToFile(filename, data_list):
    '''
    save data of list into file
    '''
    file_object = open(filename, 'a')
    try:
        file_object.writelines(data_list)
    finally:
        file_object.close()
    return len(data_list)


def pickData(conn, sql, filename):
    '''
    pickdata from database,
    save data into file
    '''
    cur = conn.cursor()
    cur.arraysize = 1000  # 1000 rows from each read
    cur.execute(sql)
    cnt = 0
    f_cnt = 0
    while True:
        rows = cur.fetchmany()
        if not rows:
            break
        (save_filename, f_cnt) = getSaveFileName(filename, f_cnt, 'Datas')
        save_list = []
        for row in rows:
            save_list.append(','.join(str(item) for item in row) + '\n')
        cnt += saveToFile(save_filename, save_list)
    return cnt


def getSaveFileName(filename, f_cnt, path):
    '''
    insert date string before ext
    '''
    if f_cnt == 0:
        f_cnt = 1
    item_list = filename.split('.')
    item_list.insert(len(item_list) - 1,
                     time.strftime('%Y-%m-%d') + '-' + str(f_cnt))
    fn_save = os.getcwd() + os.sep + path + os.sep + '.'.join(item_list)
    if os.path.exists(fn_save):
        if os.path.getsize(fn_save) > 1610612736:
            f_cnt += 1
            item_list[len(item_list) -
                      2] = time.strftime('%Y-%m-%d') + '-' + str(f_cnt)
            fn_save = os.getcwd() + os.sep + path + \
                os.sep + '.'.join(item_list)
    return fn_save, f_cnt


def getFilename(filename):
    '''
    get file name from file full name
    '''
    (file_path, file_name) = os.path.split(filename)
    return file_name
