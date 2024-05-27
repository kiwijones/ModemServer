"""

this class contains the cmp port moden calls need
to send to the port and receive

"""

import time

# from colorama import Fore, Back, Style, init
# init() # colorama
from decorators import timer_decorator
from serial_port import port_check
#from comm_functions import rabbitTransaction,sendRabbit,jsonMessage
from comm_functions import jsonMessage
import pickle
from class_objects import TransactionResponse
from api_auth import Update_Retry_RequestId


def get_modem_response( ser, *args,**kwargs):    

    
    print('='*30)

    response = ''

    print(args)    
    # ser=port_check(self.port, 19200)

    print('='*30)
    if args[1] == 'cusd':
        
        response = modem_cusd(ser, args ,kwargs)

        print('Modem_cusd Response', response)

        
        pass

    elif args[1] == 'init':
        

        response = modem_at(ser, args ,kwargs)

        print('Modem_at Response', response)

        return response
        
    rabbitTransaction(f"{response}",2)

    return response


def read_until(ser, terminator='\n'):

    print(f"reading {ser.name}...")

    resp = ''

    try:
         while not (resp.endswith(terminator) or resp.endswith('\r')):  # If the string is not terminated
            tmp = ser.read().decode('utf-8')   # Read and store in a temp variable
            if not tmp:
                return resp  # timeout occured
            resp += tmp
    except:
        pass
   
    return resp


# @timer_decorator
def read_from(serialPort, *args):

    print("read_from".center(30,"*"))

    #rabbitTransaction(f"args {args}",2)
    # print('Read from')
    args_2 = 0
    # print('='*100)

    args = args[0]
    print("read_from",args)


    args_2 = args[2]

    # print(args_2,end='\n')

    noData_Count = 0

    slow_port_response = 0   #a timer is on the port response it is's consistanty slow Ii will exit out

    print("Retry: " +  args[4])
    while True:

        # if keyboard.is_pressed('q'):
        #     print("will close")
        #     break

            start = time.time()
            # print(Fore.LIGHTCYAN_EX)
            # print('*',noData_Count )
            # print(Fore.WHITE)

            strResponse = str.strip(read_until(serialPort))  # read from the serial port

            try:
              
                noData_Count += 1

                if len(strResponse) > 0:

                  
            
                    # print(Fore.RED + 'strResponse', noData_Count, len(strResponse),strResponse)
                    print('strResponse OK?', strResponse)
                                       

                    try:
                        # print("check error")
                        if strResponse.index('ERROR') > -1:
                            return strResponse

                    except: 
                        pass





                    try:

                        # print("check minimum", args[3])




                        if strResponse.index('minimum') > -1:
  
                            #rabbitTransaction(f"Minimum {strResponse}",2)

                            if args[3] == "1":   # args 3 flag to switch between live and test
                                print("Not Good: ", strResponse)   
                                  
                                return strResponse
                            else:
                                return "Transfert a l'agent 21350000000 a ete effectue avec succes. Montant STORMCREDIT 500000 Dinar. Numero de l'operation: 260012874760."
                    except: 
                        pass




                    # print('string index',strResponse.index('HCSQ'))
                    # print('0'*30)

                    try:    

                        if strResponse.index(args_2) > 0:  # if we have found what we need, for exsample Votre in string for balance 
                            print("Found: ", strResponse)
                      
                           
                            return strResponse
                       
                    except:
                        pass
                    
                    # print('1'*30)
                    # print(str(args[2]))
                    try:
                        if args[2] == "WAITFOR":
                            if strResponse.isdigit():
                                print(strResponse)
                                print("+"*29)
                                return strResponse

                    except:
                        pass
                    
                  
                end = time.time()

                # portTimeOut = 3
                
                # portTimeOut = 30
                # print(f"Port Timeout: {portTimeOut} ")
                
                # print('2'*30)

                if end-start > 15:
                    slow_port_response += 1

                    print(f"Port Response {end-start} | {slow_port_response}")
              
                
#args[2] == "WAITFOR"
                    if slow_port_response > 3: 
                        # will exit here, modem will responsd very quickly ... milli seconds not seconds
                        return "-2 Slow Response"

                time.sleep(.1)
                # print('3'*30)
                if noData_Count > 75:
                    return "-1 No Response"

                           
            except Exception as ex:
                print(ex)
                return "-1 No Response " + ex

# @timer_decorator
def read_from_logger(serialPort, logger,settings, *args):


    print("*** read_from_logger ***")
    print(settings)

    #rabbitTransaction(f"args {args}",2)
    # print('Read from')
    args_2 = 0
    # print('='*100)

    args = args[0]

    print("read_from",args)


    args_2 = args[2]

    print('Retry: ' + str(args[3]))
    print('RequestId: ' + str(args[5]))

    # print(args_2,end='\n')

    noData_Count = 0

    slow_port_response = 0   #a timer is on the port response it is's consistanty slow Ii will exit out
    slow_port_response_timeout = 3




    try:
        with open("C:/System/Data/nocount_timeout.pck","rb") as data_file:

            print("found pickle timeout: " + str(noData_TimeOut))

            noData_TimeOut = pickle.load(data_file)
            try:
                slow_port_response_timeout = pickle.load(data_file)
            except:
                pass

    except Exception as ex:
        print("No pickle", ex)
        noData_TimeOut = 75

    print("noData_TimeOut",noData_TimeOut)

    while True:




            time.sleep(1.3)
            print("-"*100)
            start = time.time()
            print('*',noData_Count )
            strResponse = str.strip(read_until(serialPort))  # read from the serial port
            print("strResponse", strResponse)


            #print(args)
            #print(args_2)
            # if len(strResponse) > 0:

            #     if(strResponse.find("RSSI") > 0 or strResponse.find("GSM") > 0):
            #         pass
            #     else:
            #             result = logger.writelog("Modem_commands",f"Modem Response {strResponse}")  
            #             msg = jsonMessage("C",f"{result}")
            #             sendRabbit(msg,"D")


            try:
                print('--- Try --- ' + str(noData_Count))
                noData_Count += 1
                
                # try:
                #     Update_Retry_RequestId(settings,args[5],args[3])    
                # except Exception as ex:
                #     print(ex)
                
                if int(noData_Count) > int(noData_TimeOut):

                    # if thr transaction retry counter is greater that pickle timeout
                    # then the retry count will be inicremented 
                    # this retry value I may move into the settings .json
                    # retry is in the flexyTransactions table

                    try:
                        print(f'*** Update_Retry_RequestId {noData_Count} ***')

                        Update_Retry_RequestId(settings,args[5],args[3])    
                    except Exception as ex:
                        print(ex)
                    
                    return "-1 No Response"


                if len(strResponse) > 0:
                    
                    cmdFilter = ["RSSI","HCSQ","OK","'OK'"]

                    
                    #result = logger.writelog("Modem_commands",f"Modem Response: {args[5]} --> {strResponse}")

                    writeLog = True  
                    for i in cmdFilter:
                        print(i)
                        if strResponse.rfind(i) > 0:
                            writeLog = False
                            print(i)

                   
                    #if writeLog:
                    #    msg = jsonMessage("C",f"{result}")

            
                 
                    try:
                        # print("check error")
                        if strResponse.index('ERROR') > -1:
                            return "-1," + strResponse

                    except: 
                        pass


                    try:

                        # print("check minimum", args[3])

                        # result = logger.writelog("Modem_commands",f"Simulated mode {args[3]}")
                        # msg = jsonMessage("C",f"{result}")
                        # sendRabbit(msg,"D")



                        if strResponse.index('minimum') > -1:
  
                            print("Not Good: ", strResponse)   
                                  
                            return "-1," + strResponse
                            
                            # rabbitTransaction(f"Minimum {strResponse}",2)

                            # if args[3] == False:   # args 3 flag to switch between live and test

                            #     print("Not Good: ", strResponse)   
                                  
                            #     return strResponse
                            # else:
                                
                            #     result = logger.writelog("Modem_commands",f"Transaction failed, minimum value, sumulated success")
                            #     msg = jsonMessage("C",f"{result}")
                            #     sendRabbit(msg,"D")
                            # #           Transfert a l'agent 213558077860 a ete effectue avec succes. Montant STORMCREDIT 200000 Dinar. Numero de l'operation: 240018987348.
                            #     return "Transfert a l'agent 21350000000 a ete effectue avec succes. Montant STORMCREDIT 500000 Dinar. Numero de l'operation: 260012874760."
                    except Exception as ex:  
                        # a valueError will be thrown here if the value is not found
                        # we will do nothing
                        pass
                        #print('strResponse.index(minimum) > -1:' + ex)

                    # print('string index',strResponse.index('HCSQ'))
                    # print('$'*30)

                    #print("222")

                    try:    
                        # if we have found what we need, for example Votre in string for balance 
                        if strResponse.index(args_2) > 0:  
                            print(f"Found: {args_2} --> {strResponse}")
                            return "0," + strResponse.replace("'","")
                       
                    except Exception as ex:
                        pass
                        #print('strResponse.index(args_2) > 0 : ' + ex)

                    
                    try:

                        if strResponse.find("destinataire") > 0:
                            return "-3," + strResponse
                        pass     
                    except Exception as ex:
                        pass
                        #print('strResponse.find("destinataire") > 0: ' + ex)

                    try:

                        if strResponse.find("incorrect") > 0:
                            return "-3," + strResponse
                        pass     
                    except Exception as ex:
                        pass
                        #print('if strResponse.find("incorrect") > 0: ' + ex)

                

                    # print(str(args[2]))
                    try:
                        if args[2] == "WAITFOR":
                            if strResponse.isdigit():
                                print(strResponse)
                                print("+"*29)
                                return strResponse

                    except Exception as ex:
                        pass
                        #print('if args[2] == "WAITFOR": ' + ex)

                    



                end = time.time()

                # print("end-start",end-start)    
                
                if end-start > slow_port_response_timeout:
                    slow_port_response += 1

                    print(f"Port Response {end-start} | {slow_port_response}")

        
              

#args[2] == "WAITFOR"
                    if slow_port_response > 4: 
                        # will exit here, modem will responsd very quickly ... milli seconds not seconds
                        return "-2 Slow Response"

                time.sleep(.1)  

               
                           
            except Exception as ex:
                print(ex)
                return "-1 No Response " + ex


# @timer_decorator
def modem_at(port_to_send_to, *args):

    try:


        print('modem_at'.center(30,"*"))

        # print(args)
        
        args = args[0]
        kwargs = args[1]


        print(args)
        # print(args_kwargs)

        
        print("*"*50)

        if args[0] == 'at+CIMI':
            at_bytes = b'at+CIMI'

        if args[0] == 'at+CGSN':
            at_bytes = b'at+CGSN'

        if args[0] == 'at&f':
            at_bytes = b'at&f'

        elif args[0] == 'AT^CURC=0':
            at_bytes = b'AT^CURC=0'

        elif args[0] == 'ate0':
            at_bytes = b'ate0'

        elif args[0] == 'AT+CUSD=1':
            at_bytes = b'AT+CUSD=1'

        elif args[0] == 'AT+CSCS="GSM"':
            at_bytes = b'AT+CSCS="GSM"'

        elif args[0] == 'AT+CMGF=1':
            at_bytes = b'AT+CMGF=1'

        elif args[0] == 'AT+CMEE=1':
            at_bytes = b'AT+CMEE=1'

        elif args[0] == 'AT+COPS=3,0':
            at_bytes = b'AT+COPS=3,0'

        elif args[0] == 'AT^CURC=0':
            at_bytes = b'AT^CURC=0'

        at_string = '\r'

        atCommand = at_bytes + at_string.encode('utf-8')

        print("AT CMD",atCommand)
        
        # # print(port_to_send_to) 

        port_to_send_to.write(atCommand)

        readResponse = read_from(port_to_send_to,args)

        print("modem_at readResponse", readResponse)
    
        return str(readResponse)
    except Exception as ex:
        print(ex)
        return(ex)

    # x = threading.Thread(target=read_from, args=(port_to_send_to,'ser','isdigit'))

    # x.start()
    
# @timer_decorator
def modem_cusd_Logger(port_to_send_to, logger, settings, *args):  # *args here are the kwargs passed in

    
    #print("modem_cusd_Logger(port_to_send_to, logger, settings, *args)")
    print('----- modem_cusd_Logger -----', port_to_send_to)
    print('----- modem_cusd_Logger -----', args)

    for i in args:
        print(i)

    print(args[0])  # args passed in is a tuple within a tuble (('"*570*0000#",15', 'cusd', 'Votre', '1'),)


    # print("*"*50)

    args = args[0]  # new args is the first tuple 

    print(args) 

    # print('USSDMode', args[3])
    
    at_bytes = b'at+cusd=1,'  # request a response from the modem

    if args[4] == 0:  # this if ussdmode = 0
        at_bytes = b'at+cusd=0,'



    at_string = args[0] + '\r'

    print("AT:",at_string)


    atCommand = at_bytes + at_string.encode('utf-8')

    print("CMD to Send",atCommand)
   

    port_to_send_to.write(atCommand)
    
    try:

        # gets the response from the com port
        readResponse = read_from_logger(port_to_send_to,logger,settings,args)

        try:
            readSplitter = str(readResponse).split(',')
        except Exception as ex:
            print(ex)

        
        try:
            error = readSplitter[0]

        except:
            error = "-1"

        try:
            message1 = readSplitter[1]

        except:
            message1 = ""

        try:
            message2 = readSplitter[2]

        except:
            message2 = ""

        try:
            message3 = readSplitter[3]

        except:
            message3 = ""


        trResponse = TransactionResponse(error,
                                         message1=message1,
                                         message2=message2,
                                         message3=message3)
        return trResponse
    
    except Exception as ex:
        print(ex)
        return ex

@timer_decorator
def modem_cusd(port_to_send_to, *args):


    # print('----- modem_cusd -----', port_to_send_to)


    # print(args[0])  # args passed in is a tuple within a tuble (('"*570*0000#",15', 'cusd', 'Votre', '1'),)


    # print("*"*50)

    args = args[0]  # new args is the first tuple

    # print(args) 

    # print('USSDMode', args[3])
    
    at_bytes = b'at+cusd=1,'  # request a response from the modem

    if args[3] == 0:  # this if ussdmode = 0
        at_bytes = b'at+cusd=0,'



    at_string = args[0] + '\r'

    print(at_string)


    atCommand = at_bytes + at_string.encode('utf-8')

    print("CMD to Send",atCommand)
    # print(Fore.WHITE)

    # # # print(port_to_send_to) 

    port_to_send_to.write(atCommand)
    
    readResponse = read_from(port_to_send_to,args)


    
    return readResponse



    print(cmd)
    print(args)
    print("*"*50)

    
    at_bytes = b'at+'

    at_string = cmd + '\r'

    atCommand = at_bytes + at_string.encode('utf-8')

    print("comma",atCommand)

    # print(port_to_send_to) 

    port_to_send_to.write(atCommand)
    
    
    readResponse = read_from(port_to_send_to,args[0])

    print("readResponse", readResponse)

    return readResponse

    # x = threading.Thread(target=read_from, args=(port_to_send_to,'ser','isdigit'))

    # x.start()
    
    pass


