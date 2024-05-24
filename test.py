# from asyncio import Queue
# from threading import Thread
# import pyodbc
# import sqlalchemy as sal
# import pandas as pd
# from sqlalchemy import create_engine
# import random
# from time import sleep,perf_counter
# from database import mssql_engine,mssql_conn
# from serial_port import initSerial
# from send_at import ussd_cmd
# from modem_commands import modem_cusd
# from decorators import timer_decorator,threadedQueue
# from colorama import *
# from comm_functions import sendRabbit,jsonMessage
# import datetime

import pickle
import json

# try:
#     isZone = '4'
#     print(isZone)
#     active_zones = []

#     if isZone.isnumeric():
#         print("is instance")  
#         active_zones.append(isZone)  


#     print(active_zones)
#     # f = open("c:\System\server_queue.json", "r")


#     # data = json.loads(f.read())

#     # print(data)

#     # print(data["server"])

#     # with open("C:/System/Data/rabbit.pck","wb") as data_file:
#         # pickle.dump(data["server"],data_file)
# except:
#     pass
    


li = [1492, True, 'STORMCREDIT', '400000', "l'operation:", 'CUSD: 0,"Transfert a lagent 213558075460 a ete effectue avec succes. Montant STORMCREDIT 200000 Dinar. Numero de loperation: 220021622083.",68']

print(li)

count = 0
splitter = li[5].split(':')


print(splitter[0])


# print(str(splitter[1].split()[16]).replace(".","").replace('"',''))



# for i in li:
#     print(count,i)

#     if count == 5:
        




#     count+=1


# query = f"SET NOCOUNT ON select dbo.fn_ddmmHHMMSS_Time([LastBalance]) from [dbo].[tbl_PLATFORM_Devices] where  [DeviceId] = 28"

# # query = f"  SET NOCOUNT ON update [dbo].[tbl_PLATFORM_Devices] set [Balance] = 0, " +\
# #             "[LastBalance] = case " +\
# #             f"when 0 > -1 then getdate() " +\
# #             f"else (select [LastBalance] from [dbo].[tbl_PLATFORM_Devices] where [DeviceId] = 40) " +\
# #             "end " +\
# #             f"where [DeviceId] = 40 " +\
# #             f"select dbo.fn_ddmmHHMMSS_Time([LastBalance]) from [dbo].[tbl_PLATFORM_Devices]  where  [DeviceId] = 40"


# print(query)
# engine = mssql_engine()  # imported from database.py

# conn = engine.raw_connection()
# # engine.execute(query)

# cur = conn.cursor()

# for row in cur.execute(query):
#     print(row[0])


# if row:
#     print("row")

# engine.dispose()

# print(result.fetchall())