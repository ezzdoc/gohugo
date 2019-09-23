#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import librosa
from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time
import eyed3
import decimal
import argparse
import subprocess
import datetime
from decimal import Decimal

# path to the directory (relative or absolute)
dirpath = sys.argv[1] if len(sys.argv) == 2 else r'.'

def list_file_sort(file_path):
    # os.system('ls -lT -haltr')
    # filestr = os.popen("ls -lT -haltr %s" % file_path).read()
    filestr = os.popen("ls -lT %s" % file_path).read()
    # print 'ls -lT -haltr %s' % file_path
    # print filestr
    return filestr.splitlines()

def convert_silk_file(input_dir, input_file_name, output_dir):
    # These files are encoded with the SILK codec, originally developed by Skype. They can be
    # converted by stripping out the first byte and then using the SILK decoder.

    print "convert_silk_file", input_file_name
    print input_dir, input_file_name, output_dir

    input_file_path = os.path.join(input_dir, input_file_name);
    input_file = open(input_file_path, 'rb')

    output_file_path = os.path.join(output_dir, input_file_name)
    output_file = open(output_file_path, "wb")

    with input_file as f:
        lines = f.readlines()
    #写的方式打开文件
    with output_file as f_w:
        for line in lines:
            if "/images/" in line :
                #替换
                # * [目錄](<preface.md>)              * [目錄<docs/preface>)
                # * 上一節: [Session 支援](<14.2.md>)
                # * 下一節: [使用者認證](<14.4.md>)
                line = line.replace("/images/", "/gohugo/images/")
                # print line
            elif "/img/" in line :
                 line = line.replace("/img/", "/gohugo/img/")
            elif "/share/" in line :
                 line = line.replace("/share/", "/gohugo/share/")
            elif "/css/" in line :
                 line = line.replace("/css/", "/gohugo/css/")
            elif "/fonts/" in line :
                 line = line.replace("/fonts/", "/gohugo/fonts/")
            f_w.write(line)
    input_file.close()
    output_file.close()

def rename_file(file_path, filelist):

    now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    converted = now + "_converted"
    os.mkdir(converted)

    filelen = len(filelist)
    index = 0
    index_real = 1
    while index < filelen:
        itemstr = filelist[index]
        index+=1
        if (".md" in itemstr):

            # print fileitem
            attrlist = itemstr.split()
            attrlen = len(attrlist)
            attr_time = attrlist[attrlen-3]
            attr_name = attrlist[attrlen-1]
            attr_index = "%03d" % index_real
            index_real+=1
            # file_name = (attr_index+"_"+attr_time+"_duration_"+attr_name).replace(':','')
            # print file_name
            # old_file = os.path.join(file_path, attr_name)
            # new_file = os.path.join(file_path, file_name)
            # os.rename(old_file, new_file)
            attr_name2 = attr_name.replace('.md','')
            # print attr_name
            # print("- ["+attr_name2+"]({{< relref \"/docs/content/"+ attr_name2 +"\" >}}) ")
            convert_silk_file(file_path, attr_name, converted)

if __name__ == '__main__':
    filelist = list_file_sort(dirpath)
    # print filelist[1]
    rename_file(dirpath, filelist)
