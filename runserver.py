"""
This script runs the nCovNews application using a development server.
"""
import time
import _thread
from os import environ
from nCovNews import app
from nCovNews import db
from nCovNews import data_update
from WechatPCAPI import wxrobot

def thread_robot():
    wxrobot.init()

if __name__ == '__main__':
    
    # 数据库测试
    # db.drop_all()
    db.create_all()

    # 实时数据更新
    data_update.auto_update( 30*60 )
    # 启动服务器
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    time.sleep(1)
    # 启动机器人
    _thread.start_new_thread(thread_robot)
    time.sleep(1)
    # 启动本地网页
    app.run(HOST, PORT)
