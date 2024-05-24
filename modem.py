import keyword
import threading
import serial_port
import time
import serial.tools.list_ports
import logging
import random
import math
from decorators import timer_decorator
from serial_port import port_check
#from comm_functions import rabbitTransaction,sendRabbit,jsonMessage
from comm_functions import rabbitTransaction,jsonMessage
import pickle

from database import mssql_engine

from serial_port import initSerial


def get_single_port(port):

    server = "0.0"

    try:
        with open("C:/System/Data/rabbit.pck","rb") as data_file:
               server = pickle.load(data_file)
               
    except:
            
            pass

    query = "select [DeviceId],rtrim([ComPort]),isnull([SimPin],'0000'),[DeviceReference],[ZoneId],[DeviceDetail],isnull([IMEI],'?') as IMEI " +\
        "from [dbo].[tbl_PLATFORM_Devices] " +\
        f"where [ZoneId] > 0 and [server] = '{server}' and rtrim([ComPort]) = '{port}'"

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


#ports = ["COM38","COM33","COM41"]

ports = ["COM1"]

# port = get_single_port("COM38")

# print(port)


class Response:
     
     def __init__(self):
        self.at_string = '\r'
     
     def ok_response(self):
        
        while 1:
            
            if ser.in_waiting > 0:

                data_raw =  ser.readline()

                if str(data_raw).find("OK"):
                     print("True")
                     return True
                else:
                     return False
          

     def balance_response(self):
         print("balance Response")
         counter = 0
         while 1:
            
            # if ser.in_waiting > 0:

                data_raw =  ser.readline()

                # if str(data_raw).find("OK"):
                #      print("True")
                #      return True
                # else:
                #      return False
                print(f"{counter} {data_raw}")

                if str(data_raw).find("CUSD:") > 0:

                    counter = -1

                    return str(data_raw)

                if str(data_raw).find("CME") > 0:
                    counter = -1

                    return str(data_raw)
                     

                if str(data_raw).find("Votre") > -1:
                   
                    counter = -1

                    return str(f"{counter} {data_raw}")

               

                # print(counter)
                # time.sleep(.1)

                # if counter == -1:
                #     break
                if counter > 75:
                    print("No Reply")
                    return "No Reply"
            
                counter += 1
    
class ModemInit(Response):
    
    def __init__(self,ser):
        self.ser = ser

    def modem_init(self):
        atcmds = [b'at',
                  b'at&f',
                  b'AT^CURC=0',
                  b'ate0',
                  b'AT+CUSD=1',
                  b'AT+CMGF=1',
                    b'AT+COPS=3,0',
                    b'AT+CSCS="GSM"',
                    b'AT+CMEE=1',
                    b'AT+COPS=3,0',
                    ]
         
        for cmds in atcmds:
             
            at_bytes =  cmds
            atCommand = at_bytes + self.at_string.encode('utf-8')

            print("AT CMD",atCommand)

            # # print(port_to_send_to) 

            ser.write(atCommand)

            mr = ModemRead(ser)
            time.sleep(1)
            mr.ok_response()
         
    def modem_reset(self):
        atcmds = [b'at',b'at&f',
                  b'AT+CFUN=0',
                  b'wait',
                  b'AT+CFUN=1'
                  ]
        
        for cmds in atcmds:
             

            # print(self.ser)
            at_bytes =  cmds


            if(str(cmds).find("wait") == -1):
                 
                atCommand = at_bytes + self.at_string.encode('utf-8')
                print("AT CMD",atCommand)

                ser.write(atCommand)

                response = self.ok_response()



                print(response)


            else:
                 time.sleep(10)


            

            print("AT CMD",atCommand)

class ModemRead(Response):
    
    def __init__(self,ser):
          self.ser = ser

    def modem_init(self):
        atcmds = [b'at',b'at&f',
                  b'AT^CURC=0',
                  b'ate0',
                  b'AT+CUSD=1',
                  b'AT+CMGF=1',
                    b'AT+COPS=3,0',
                    b'AT+CSCS="GSM"',
                    b'AT+CMEE=1',
                    b'AT+COPS=3,0',
                    ]
         
        for cmds in atcmds:
             
            at_bytes =  cmds
            atCommand = at_bytes + self.at_string.encode('utf-8')

            print("AT CMD",atCommand)

            # # print(port_to_send_to) 

            ser.write(atCommand)

            mr = ModemRead(ser)
            time.sleep(1)
            mr.ok_response()
          
          
    def ok_response(self):
        okCounter = 0
        while 1:
            
            
            if ser.in_waiting > 0:

                data_raw =  ser.readline()

                if str(data_raw).find("OK"):
                     print("True")
                     return True
                else:
                     return False
                
        
    def balance_response(self):
         print("balance Response")
         counter = 0
         while 1:
            
            # if ser.in_waiting > 0:

                data_raw =  ser.readline()

                # if str(data_raw).find("OK"):
                #      print("True")
                #      return True
                # else:
                #      return False
                print(f"{counter} {data_raw}")

                if str(data_raw).find("CUSD:") > 0:

                    counter = -1

                    return str(data_raw)

                if str(data_raw).find("CME") > 0:
                    counter = -1

                    return str(data_raw)
                     

                if str(data_raw).find("Votre") > -1:
                   
                    counter = -1

                    return str(f"{counter} {data_raw}")

               

                # print(counter)
                # time.sleep(.1)

                # if counter == -1:
                #     break
                if counter > 75:
                    print("No Reply")
                    return "No Reply"
            
                counter += 1
         
    


for c in ports:



    ser = initSerial(c,19200)

    reset = ModemInit(ser)
    reset.modem_reset()









# for c in ports:



#     ser = initSerial(c,19200)

#     atcmds = [b'AT+CIMI',b'AT+CUSD=0',b'AT+CUSD=1',b'AT+CSCS="GSM"',b'AT+CUSD=2',b'at+cusd=1,"*570*0000#",15']

#     # b'AT+CSCS="IRA"',
#     # b'AT+CUSD=0',b'AT+CUSD=1',

#     print(ser.isOpen())

#     print(c)
#     print("*"*50)
#     ser.flushInput()
#     ser.flushOutput()
#     at_string = '\r'
#     # at_bytes = b'at+cusd=1,"*570*0000#",15'

#     mr = ModemRead(ser)
    
#     mr.modem_init()

#     for cmds in atcmds:
         
#         # ser.flushInput()
#         # ser.flushOutput()


#         at_bytes =  cmds
#         atCommand = at_bytes + at_string.encode('utf-8')

#         print("AT CMD",atCommand)

#             # # print(port_to_send_to) 
#         response = ""

#         if(str(atCommand).find("570") > 0):
        
#             ser.write(atCommand)

#             response = mr.balance_response()


#         else:
#              ser.write(atCommand)
#              response = mr.ok_response()

     
            

             
#         # print(type(response))
#         print(response)
#         time.sleep(.5)







# strPort = []


# ser = initSerial(self.port[1],19200)

# print(ser.isOpen())














