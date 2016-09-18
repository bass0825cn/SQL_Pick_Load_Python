from MyTools import *
import os
import subprocess

file_list = searchFile(os.getcwd() + os.sep + 'Datas', '.txt')
print file_list
zip_file = os.getcwd() + os.sep + 'Outputs' + os.sep + '123.zip'
cmd = ['winrar', '-phangar']
cmd.append(zip_file)
print cmd + file_list
print ' '.join(cmd + file_list)
subprocess.call(cmd + file_list)

