
import os
import sys
import cx_Oracle

def searchFile(path, word):
        '''
        Get File List
        '''
        filelist = []
        for filename in os.listdir(path):
                fp = os.path.join(path, filename)
                if os.path.isfile(fp) and word in filename:
##                        print fp
                        filelist.append(fp)
                elif os.path.isdir(fp):
                        searchFile(fp, word)
        return filelist

def connectOracle(username, password, tnsname):
        return cx_Oracle.connect(username, password, tnsname)


currentDir = os.getcwd() + "\\Datas"
fl = searchFile(currentDir, ".txt")
print fl
