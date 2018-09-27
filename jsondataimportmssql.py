import pymssql
import json

class db:
    def __init__(self,server,user,pwd,database):
        self.server = server
        self.user = user
        self.pwd = pwd
        self.database = database
    
    def __getconnect(self):
        self.conn = pymssql.connect(self.server,self.user,self.pwd,self.database)
        cur = self.conn.cursor()
        if not cur:
            raise NameError("连接数据库失败")
        else:
            return cur
    
    def execute(self,sql):
        cur = self.__getconnect()
        cur.execute(sql)
        resultdata = cur.fetchall()
        self.conn.close()
        return resultdata
    
    def exe_many(self,sql,params):
        cur = self.__getconnect()
        cur.executemany(sql,params)
        self.conn.commit()
        self.conn.close()

SERVER = "192.168.2.37"
USER = "sa"
PWD = "sa123456"
DATABASE = "CountyMianStatistics"

def get_entitys():
    msdb = db(SERVER,USER,PWD,DATABASE)
    data = msdb.execute("select * from AnalysisOfRiceSalesStage")
    for row in data:
        print('row = %r' % (row,))

def jsontoobj(jsonstr):
    json_str = json.dumps(jsonstr)
    data = json.loads(json_str)
    return data

def insert(sql,params):
    msdb = db(SERVER,USER,PWD,DATABASE)
    msdb.exe_many(sql,params)

if __name__ == '__main__':
    #get_entitys()
    data = [
        {'value':70,'name':'勉县同沟寺镇农业服务站管沟服务部'   },
        {'value':74,'name':'勉县黄沙农资经营部'                 },
        {'value':75,'name':'同沟寺李正华'                       },
        {'value':75,'name':'勉县翠芳新丰农资服务部'             },
        {'value':78,'name':'元墩桩家医院'                       },
        {'value':78,'name':'勉县镇川农资经营部'                 },
        {'value':81,'name':'勉县农民丰农资经营部'               },
        {'value':85,'name':'老道寺张氏种子店'                   },
        {'value':90,'name':'周家山来新忠'                       },
        {'value':102,'name':'勉县农业生产资料有限公司第二庄家医院'}
    ]

    obj = jsontoobj(data)
    param = []
    for item in obj:
        param.append((item["name"],item["value"]))
    insert("INSERT INTO VarietyRecordNumber VALUES (%s, %d)",param)
