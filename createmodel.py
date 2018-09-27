#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:WangLe

import os
import pymssql
import json
#const
path = 'C:\\Models\\'

#read db
class db:
    def __init__(self,server,database,user,pwd):
        self.server = server
        self.database = database
        self.user = user
        self.pwd = pwd
    
    def __getconnection(self):
        self.conn = pymssql.connect(self.server,self.user,self.pwd,self.database)
        cur = self.conn.cursor()
        if not cur:
            raise NameError('db connection error!')
        else:
            return cur
    
    def readdata(self,sql):
        cur = self.__getconnection()
        cur.execute(sql)
        resultdata = cur.fetchall()
        self.conn.close()
        return resultdata

#abstract
def create_abstract_class():
    classname = input('enter abstract class name:')
    prop = input('enter property name:')
    propType = input('enter property Type:')
    filename = classname + '.cs'
    ispathexist = os.path.exists(path)
    if not ispathexist :
        os.mkdir(path)
    with open(os.path.join(path,filename),'w+') as fd:
        fd.write('namespace {0}\n'.format(ns))
        fd.write('{\n')
        fd.write('    public abstract class {0}\n'.format(classname))
        fd.write('    {\n')
        fd.write('        public '+propType+' '+prop+' { get; protected set; }\n')
        fd.write('    }\n')
        fd.write('}\n')
    return (classname,prop)

#models
def create_model_class(ns,classname,props,isextends = False,abstractname = '',abstractpropname = ''):
    if not isinstance(props,list) :
        raise NameError('create_model_class param type error(props type is '+str(type(props))+')')
    filename = classname + '.cs'
    with open(os.path.join(path,filename),'w+') as fd:
        fd.write('namespace {0}\n'.format(ns))
        fd.write('{\n')
        if isextends :
            fd.write('    public partial class {0} : {1}\n'.format(classname,abstractname))
        else:
            fd.write('    public partial class {0}\n'.format(classname))
        fd.write('    {\n')
        for prop in props:
            cloumnname = prop[0]
            datatype = prop[1].lower()
            isnullable = prop[2].lower()
            if cloumnname == abstractpropname:
                continue
            if datatype == 'int':
                if isnullable == 'yes':
                    datatype = 'int?'
                else:
                    datatype = 'int'
            elif datatype == 'datatime':
                if isnullable == 'yes':
                    datatype = 'DateTime?'
                else:
                    datatype = 'DateTime'
            elif datatype == 'decimal' or datatype == 'float':
                if isnullable == 'yes':
                    datatype = 'double?'
                else:
                    datatype = 'double'
            else:
                datatype = 'string'
            fd.write('        public '+ datatype +' '+cloumnname+' { get; set; }\n')
        fd.write('    }\n')
        fd.write('}\n')

if __name__ == '__main__':
    ser = input('enter db server:')
    database = input('enter db name:')
    user = input('enter db user name:')
    pwd = input('enter db user password:')
    ns = input('enter namespace:')
    isabstract = input('create abstract class?(y/n):')
    abstractclassname = ''
    abstractclasspropname = ''
    if isabstract.lower() == 'y':
        abstractclassname,abstractclasspropname = create_abstract_class()
    
    entertable = input('enter table name(empty for all):')
    msdb = db(ser,database,user,pwd)
    if entertable.strip() == '':
        tablesdata = msdb.readdata('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES')
        for row in tablesdata:
            cloumnsdata = msdb.readdata("SELECT COLUMN_NAME,DATA_TYPE,IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+row[0]+"'")
            if isabstract.lower() == 'y':
                create_model_class(ns,row[0],cloumnsdata,True,abstractclassname,abstractclasspropname)
            else:
                create_model_class(ns,row[0],cloumnsdata)
    else:
        for tablename in entertable.split(','):
            cloumnsdata = msdb.readdata("SELECT COLUMN_NAME,DATA_TYPE,IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+tablename+"'")
            if isabstract.lower() == 'y':
                create_model_class(ns,row[0],cloumnsdata,True,abstractclassname,abstractclasspropname)
            else:
                create_model_class(ns,row[0],cloumnsdata)