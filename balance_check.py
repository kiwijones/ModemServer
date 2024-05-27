from asyncio import Queue
from threading import Thread
import pyodbc
import sqlalchemy as sal
import pandas as pd
from sqlalchemy import create_engine
import random
from time import sleep,perf_counter
from database import mssql_engine
from serial_port import initSerial
from send_at import ussd_cmd
from modem_commands import modem_cusd,modem_cusd_Logger,get_modem_response
from decorators import timer_decorator,threadedQueue
from colorama import *
#from comm_functions import sendRabbit,jsonMessage
from comm_functions import jsonMessage
import datetime
from class_objects import Logging_File
import shelve
import pickle
from api_auth import ModemBalance


def run_balance(port):
    print(f"Port {port}")

def get_active_ports():

    server = "0.0"

    try:
        with open("C:/System/Data/rabbit.pck","rb") as data_file:
               server = pickle.load(data_file)
               
    except:
            
            pass

    query = "select [DeviceId],rtrim([ComPort]),isnull([SimPin],'0000'),[DeviceReference],[ZoneId],[DeviceDetail],isnull([IMEI],'?') as IMEI,[DeviceNumber] " +\
        "from [dbo].[tbl_PLATFORM_Devices] " +\
        f"where [ZoneId] > 0 and [server] = '{server}' " # and rtrim([ComPort]) = 'COM38'"


    print(query)

    msg = jsonMessage('C',f"{query}")  # send the queue to rabbit

    #sendRabbit(msg,"D")

    engine = mssql_engine()  # imported from database.py
    conn = engine.raw_connection()

    cur_known = conn.cursor()

    result = cur_known.execute(query).fetchall()

    # result = engine.execute(query)
    # engine.commit()
   
    return result


def get_single_port(port):

    server = "0.0"

    try:
        with open("C:/System/Data/rabbit.pck","rb") as data_file:
               server = pickle.load(data_file)
               
    except:
            
            pass

    query = "select [DeviceId],rtrim([ComPort]),isnull([SimPin],'0000'),[DeviceReference],[ZoneId],[DeviceDetail],isnull([IMEI],'?') as IMEI,[DeviceNumber] " +\
        "from [dbo].[tbl_PLATFORM_Devices] " +\
        f"where [ZoneId] > 0 and [server] = '{server}' and rtrim([ComPort]) = {port}"

    print(query)

    msg = jsonMessage('C',f"{query}")  # send the queue to rabbit

    #sendRabbit(msg,"D")

    engine = mssql_engine()  # imported from database.py
    conn = engine.raw_connection()

    cur_known = conn.cursor()

    result = cur_known.execute(query).fetchall()

    # result = engine.execute(query)
    # engine.commit()
   
    return result
#@timer_decorator

def set_RemoteBalance(settings,comPort,ismiResponse, balance):
     
     ModemBalance(settings['AccountId'],comPort,1,ismiResponse, balance)

def set_balance(deviceId, balance,logger, server):


    # print(jsonMessage("C","Hello"))


    # print(Fore.GREEN)
    print(f"Setting balance {deviceId} {balance} {server}")
    # sendRabbit(f"Setting balance {deviceId} {balance}","D")
    # print(Fore.WHITE)
    
    try:


        query = f"update [dbo].[tbl_PLATFORM_Devices] set [Balance] = {balance}, " +\
            f"[Server] = '{server}', "+ \
            "[LastBalance] = case " +\
            f"when {balance} > -1 then getdate() " +\
            f"else (select [LastBalance] from [dbo].[tbl_PLATFORM_Devices] where [DeviceId] = {deviceId}) " +\
            "end " +\
            f"where [DeviceId] = {deviceId} "
            #f"select dbo.fn_ddmmHHMMSS_Time([LastBalance]) from [dbo].[tbl_PLATFORM_Devices]  where  [DeviceId] = {deviceId}"


        # print(query)

        
        msg = jsonMessage('C',f"{query}")  # send the queue to rabbit

        sendRabbit(msg,"D")

        logger.writelog("set_balance",f"{query}")

        engine = mssql_engine()

        conn = engine.raw_connection()

        # trans = conn.begin()

        result = conn.execute(query)

        conn.commit()

        print(result)

        conn.close()
        
        result.close()
        print('00')
        query = f"SET NOCOUNT ON select dbo.fn_ddmmHHMMSS_Time([LastBalance]) from [dbo].[tbl_PLATFORM_Devices] where  [DeviceId] = {deviceId}"
        
        print(query)
        engine1 = mssql_engine()  # imported from database.py

        conn = engine1.raw_connection()
        # engine.execute(query)

        cur = conn.cursor()

        for row in cur.execute(query):
            print('row',row[0])
            print('11')
            return row[0]

        
                
        

    except Exception as ex:
        print('set_balance ERROR', ex)
        # print(Fore.WHITE + '')

def get_balance( ser, logger,settings, *args,**kwargs):    


    response = ''
    
    # ser=port_check(self.port, 19200)
    print(args)
    try: 
        if args[1] == 'cusd':
            
            # response = modem_cusd(ser, args ,kwargs)
            response = modem_cusd_Logger(ser, logger,settings,args ,kwargs)

            pass
    except Exception as ex:
        print("Error opening port")

   
    return response


class BC():

    def __init__(self, logger, modem):

        try:
            with open("C:/System/Data/rabbit.pck","rb") as data_file:
               server = pickle.load(data_file)
               self.server = server 
        except:
            self.server = '0.0'
            pass
        
        try:
            with open("C:/System/Data/settings.pck","rb") as data_file:
               settings = pickle.load(data_file)
              
               self.accountId = settings['AccountId']
        except:
            self.server = '0.0'
            pass
        

        self.port = modem['port']   # (28, 'COM41', '0000', '603032658220983', '5', 'NADIA', '867444030261376')
        self.imei = modem['IMSI']
        self.logger = logger
        self.settings = settings
        self.modem = modem


        print('__INIT__ : ' + self.port + " " + self.accountId)

    def port_balance(self):

            print('self')
            print(self.port)
            print(self.settings)
            print(self.accountId)

            strPort = []

            ser = initSerial(self.port,19200)

            print(ser.isOpen())
           
            current_time = datetime.datetime.now().strftime("%H:%M:%S")

            if(ser.isOpen()):

                print(self.modem["balanceAt"])

            #port[2] is the sim pin
                response = get_balance(ser,self.logger,self.settings,f'"*{self.modem["balanceAt"]}*{str(self.modem["simPin"])}#",15','cusd','Votre',False,'1',self.port[1])
                


                balance_message =  str(response.message2).split(" ")


                #response1 = self.logger.writelog("get_balance",f"{self.port[1]} {response}")

                #msg = jsonMessage('C',f"{response1}")  # send the queue to rabbit

                #sendRabbit(msg,"D")

                try:
                    
                    #if response[0].isdigit() or response[0] == "-1" or response[0] == "-2":
                    if  response.errorCode == -1 or response.errorCode == -2:
                            # print("AAAAAAAA")
                            print('Error:', response[0], self.port[0])
                            
                            err = -1

                            if response[0] == "-2":
                                err = -2

                            lastDate = set_balance(self.port[0],err,self.logger,self.server)  # setting balance t0 -1 inducate error

                            # print(Fore.WHITE + '')
                            
                            strPort.append(str(self.port[0]) + ',' + str(self.port[7]) + ','+ str(self.port[1]) + ',' + str(err) + ',' +  lastDate + "," + str(self.port[4])+ "," + str(self.port[5])+ ",True")
                            print(strPort)
                            # type BA is for balance array 
                            msg = jsonMessage('BA',' '.join(map(str,sorted(strPort))))  # send the queue to rabbit
                            #sendRabbit(msg,"D")  # D here is dashboard    
                            return strPort
                    else:
                        # print("BBBBBBBB")
                        try:
                           # 28,867444030261376,COM44,800000,22/02/2023 08:13:43,5,NADIA,True
                            if balance_message[4].isdigit(): # if a -1 is received then its a possible slow response from the
                                
                                lastDate = set_RemoteBalance(self.settings, self.port,self.imei,balance_message[4])

                                #lastDate = set_balance(self.port[0],response[5],self.logger, self.server)  

                                # print('rowcount',lastDate)
                               # below is what is sent to rabbit
                                #strPort.append(str(self.port[0]) + ',' + str(self.port[7]) + ','+ str(self.port[1]) + ','+ str(response[5]) + ',' +  str(lastDate) + "," + str(self.port[4]) + "," + str(self.port[5])+",True")
                            else:
                            
                                strPort.append(str(self.port[0]) + ',' + str(self.port[7]) + ','+ str(self.port[1]) + ',-1,' +  str(current_time) + "," + str(self.port[4]) + "," + str(self.port[5]) +",True")
                            
                               

                        except Exception as ex:
                            
                            print("get_balance:", ex) 
                            

                except Exception as ex:
                    rowCount = set_balance(self.port[0],-2,self.logger,self.server) 
                    print(ex)
                    print("-"*30)
            else:
                print("serial port closed")
                strPort.append(str(self.port[0]) + ',Closed,'+ str(self.port[1]) + ',-1,' +  str(current_time) + ',Closed,0,0')
            # '28,867444030261376,COM41,90000,09/03/2023 12:36:57,5,COD NADIA,True'
            #msg = jsonMessage('BA',' '.join(map(str,sorted(strPort))))  # send the queue to rabbit
            #sendRabbit(msg,"D")  # D here is dashboard
            return strPort

class BalanceCheck():
    '''This will loop through all active ports, getitng the current balance from the sim card
    update the database with new balance and last balance date'''
    
    def __init__(self,settings):

        settings['Balance'] = False    
        # setting_file.write_setting_file(False,False)

        Threadedbalance(settings)
                
    
def task(id):
    print(f'Starting the task {id}...')
    sleep(1)
    print(f'The task {id} completed')

# @threadedQueue
def taskBalance(que,logger, modem):

    print(f"started {modem['port']}")

    #return

    bal = BC(logger, modem)  

   
    result = bal.port_balance()
        
        
    # bal.get()
   

    # print(result)

    if len(str(result)) > 10:  # result can come back with None... so drop that
        que.append(result)

# calling witn modem list
def Threadedbalance( modems):  # <-- modems is the modems.pickle... modems.json

        with open("C:/System/Data/nocount_timeout.pck","wb") as data_file:
            pickle.dump(75,data_file)  # modem timeout
            pickle.dump(4,data_file)   # slow response
        
        threads = []  # thread list
        que = []  #que list, this object is passed into the threaded task where it gets appended to

        logger = Logging_File()

        for modem in modems:

            print(modem)

            if modem["port"] != "com8":    
                taskBalance(que,logger, modem)


            #return

            # t = Thread(target=taskBalance,args=(modem['port'],que,logger,modems))
            
            # # print(t)
            # threads.append(t)
            # t.start()

                
        for t in threads:
            
            t.join()  # wait for all threads to complete
        
        active_zones = []

        for q in que: 
            
            isZone =   q[0].split(',')[5]  

            if isZone.isnumeric():
                active_zones.append(int(isZone))

            print(q)  # loop through the queue

        print(active_zones)
        with open("C:/System/Data/active_zones.pck","wb") as data_file:
            pickle.dump(active_zones,data_file)
            

        msg = jsonMessage('DW','|'.join(map(str,sorted(que))))  # send the queue to rabbit
        #sendRabbit(msg,"D")  # D here is dashboard

if __name__ == "__main__":


    try:
     
        with open('C:/System/Data/modems.pck', 'rb') as file:
            # Unpickle the data
            modems = pickle.load(file)

            #print(modems)

            #for modem in modems:   
                
                #print(modem)


            # pass the modem list 
            Threadedbalance(modems)
            
    except Exception as ex:
            print(ex)

                         


    # shelve_one = 'C:/System/Data/shelve_one.shlv'

    # running_shelve = shelve.open(shelve_one, flag='w')  

    # Threadedbalance(running_shelve)
