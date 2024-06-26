# import pyodbc
import json
import sqlalchemy as sal
import pandas as pd
from sqlalchemy import create_engine
# import random
from database import mssql_engine
from serial_port import initSerial
#from comm_functions import sendRabbit,jsonMessage,rabbitTransaction,is_integer
from comm_functions import jsonMessage,rabbitTransaction,is_integer
from modem_commands import modem_cusd,modem_cusd_Logger
from decorators import timer_decorator,logger,Sendmail_Decorator,Sendmail_Decorator_2

from class_objects import Logging_File,TransactionResponse

from time import sleep
import shelve
import pickle,os
import api_auth 
import http.client
import requests

# @logger

# # @Sendmail_Decorator('Process Exception')

# @timer_decorator

# added 15/04/2023
def updateRetry_Request(requestId, retry):

    value = int(retry) + 1

    if value > 3:
        value = -1

    print(value)

    query = "set nocount on update [dbo].tbl_GATEWAY_FlexyTransactions " +\
        f"set retry = {value} " +\
            f"where requestID = {requestId}"
    

    engine = mssql_engine()
    conn1 = engine.raw_connection()
    cursor = conn1.cursor()
    result = cursor.execute(query)
    cursor.commit()
    cursor.close()
    del cursor


def updateRetry(transactionId, retry):

    value = int(retry) + 1

    if value > 3:
        value = -1

    print(value)



    #api_auth.Update_Retry_TransactionId(sett)

    # query = "set nocount on update [dbo].tbl_GATEWAY_FlexyTransactions " +\
    #     f"set retry = {value} " +\
    #         f"where TransactionID = {transactionId}"
    

    # engine = mssql_engine()
    # conn1 = engine.raw_connection()
    # cursor = conn1.cursor()
    # result = cursor.execute(query)
    # cursor.commit()
    # cursor.close()
    # del cursor

    # print(query)
    # print(result)



def any_new_transactions(logger, settings):


    api_auth.AnyTransactions_ForAccount(settings)

    # # query = "set nocount on select fr.[RequestId],fr.[PhoneNumber],fr.[Amount],fr.[ZoneId],rtrim([ComPort]) as ComPort,ft.SessionId,convert(int,pa.CreditBalance) as CreditBalance,pa.AccountName,pa.AccountCode,ft.TransactionID,ft.retry,pd.DeviceId " +\
    # #     "from [dbo].[tbl_GATEWAY_FlexyRequests] fr " +\
    # #         "join [dbo].[tbl_PLATFORM_Devices] pd on fr.[ZoneId] = pd.ZoneId " + \
    # #             "join [dbo].tbl_GATEWAY_FlexyTransactions ft on fr.RequestID = ft.RequestId " + \
    # #                 "join [Bluechip].dbo.tbl_PLATFORM_Sessions ps on ft.SessionId = ps.SessionID "  +\
    # #                     "join [Bluechip].dbo.tbl_PLATFORM_Accounts pa on ps.AccountID = pa.AccountID " +\
    # #                         "where fr.[Status] = 0 and ft.retry > -1 "

    # query = '''
    # set nocount on select fr.[RequestId],fr.[PhoneNumber],fr.[Amount],fr.[ZoneId],rtrim([ComPort]) as ComPort,
    # ft.SessionId,convert(int,pa.CreditBalance) as CreditBalance,pa.AccountName,pa.AccountCode,ft.TransactionID,ft.retry,pd.DeviceId,
    # convert(int,pd.[Balance])
    # from [dbo].[tbl_GATEWAY_FlexyRequests] fr
    # join [dbo].[tbl_PLATFORM_Devices] pd on fr.[ZoneId] = pd.ZoneId
    # join [dbo].tbl_GATEWAY_FlexyTransactions ft on fr.RequestID = ft.RequestId
    # join [Bluechip].dbo.tbl_PLATFORM_Sessions ps on ft.SessionId = ps.SessionID
    # join [Bluechip].dbo.tbl_PLATFORM_Accounts pa on ps.AccountID = pa.AccountID
    # where fr.[Status] = 0 and ft.retry > -1 and fr.[Amount] <= convert(int,pd.[Balance])
    # order by fr.[RequestId] desc
    # '''

    # # print(query)        
    # engine = mssql_engine()  # imported from database.py
    # conn = engine.raw_connection()
    # cur_known = conn.cursor()
    # result = cur_known.execute(query).fetchall()   
    # cur_known.close
    # del cur_known
    # return result



# @timer_decorator
def enoughCredit(comport, amount, zoneid):
    print(comport, amount)

    query = "select convert(int,[Balance]),[simpin] from [dbo].[tbl_PLATFORM_Devices] where [ComPort] = '" + comport + "' " +\
        "and [ZoneId] = " + str(zoneid)

    # query = "select [Balance],[simpin] from [dbo].[tbl_PLATFORM_Devices]"

    print(query)  

    # engine = mssql_engine()  # imported from database.py
    # conn = engine.connect()
    engine = mssql_engine()
    conn = engine.raw_connection()
    cur_known = conn.cursor()
    result = cur_known.execute(query).fetchall()
    cur_known.close()
    del cur_known
    
    msg = jsonMessage("C",f"Credit Response {result}")

    #sendRabbit(msg,"D")

    print(result)

    # return (str(result).replace('[','').replace(']','').replace(')','').replace('(',''),)

    return result

def hasAccountCredit(sessionId, amount):
    pass

# @timer_decorator
def run_Transaction( ser,logger, settings, *args,**kwargs):   


    print("run_Transaction", args) 

    with open("C:/System/Data/nocount_timeout.pck","wb") as data_file:
        pickle.dump(300,data_file)  # modem timeout
        pickle.dump(3,data_file)   # slow response

    if args[1] == 'cusd':
        
        print('modem_cusd_Logger')

        trResponse = modem_cusd_Logger(ser, logger, settings,args ,kwargs)


        #trResponse = TransactionResponse(response[0],response[1])


        print("run_balance", trResponse) 

        try:
            os.remove("C:/System/Data/nocount_timeout.pck")
        except:
            pass

        return trResponse

    #     pass
    pass

# @timer_decorator
def process_transaction(*args, logger,settings):

    print("process_transaction".center(50,"*"))

    response = ""
    response_fail = []
    args = args[0]

    print(args)

    #print(type(args))

    service_amount = args["amount"]  # RESET THIS BACK TO 0 SERVICE AMOUNT WILL BE SET FROM THE MODEM BALANCE
    service_pin = '0000'
   
    # try:
    #     python_Api_Data = json.dumps(args[0])   



    #     print(python_Api_Data)

    # except Exception as ex:
    #                 print(ex)
    
    #print(python_Api_Data)
    # try:

    #     # service_amount = int(enoughCredit(comport=args[4],amount=args[2],zoneid=args[3]))

    #     credit_response = enoughCredit(comport=args[4],amount=args[2],zoneid=args[3])
        
    #     account_Credit = hasAccountCredit(sessionId=45443, amount=args[2])


    #     print(credit_response)

    #     print(type(credit_response))
    #     # for i in credit_response:
    #     #     print(i)

    #     service_amount = credit_response[0][0]   # balance before
    #     service_pin = credit_response[0][1]

    #     # print(service_amount)
    #     # print(service_pin)
    #     rabbitTransaction(f"Available credit {service_amount}",1)
    #     result = logger.writelog("Process_transaction 19",f"Available credit {service_amount}")
    #     msg = jsonMessage("C",f"{result}")
    #     #sendRabbit(msg,"D")
        
    # except Exception as ex:
    #     print(ex)
    #     print(f"No service balance found for {args[4]} : {service_amount}")
    #     rabbitTransaction(f"No service balance found for {args[4]}",0)
    #     service_amount = -1




    #if service_amount > 0:  # Modem has credit... keep going

    print(type(service_amount))

        # print(service_amount)
   
        # print("we have an amount")
        
    print(int(service_amount))

    try:

        print(args['amount'])
        print(args['retry'])

    except Exception as ex:
        print(ex)


        #return
        #if(int(service_amount) >= int(args['amount'])):  # the modem credit is greater or equals to requested
            # print("Continue with transaction")
            
    productId = args['productId']
    phoneNo = args['phoneNumber']
    requestId = args['requestId']
    simPin = args['requestId']
    retry = args['retry']


    print(args['productId'])


    #todo map modems 
   

    #rabbitTransaction(f"Transaction amount {args[2]}",1)

    comPort = ""
    balanceAt = ""
    transactionAt = ""
    currentBalance = 0
    try:
        
        ## map the modems from the 
        with open('C:/System/Data/modems.pck', 'rb') as file:
            # Unpickle the data
            modems = pickle.load(file)

            print(modems)
            
            # Iterate over the unpickled data and get the comport for the product supplied
            for item in modems:   

                print(item['product'])

                # if get a match with the product then get the working comport & current balance 
                if(item['product'] == str(productId)):

                    try:
                        portResponse = api_auth.Get_ComportForProduct( settings,productId,args['amount'])

                        for port in json.loads(portResponse):
                                comPort = str(port["ComPort"])
                                currentBalance = port["Balance"]

                        print(comPort)

                    except Exception as ex:
                        print(ex)        
                   
        try:

            print("==================================================================================")
            print("==================================================================================")

            if(int(currentBalance) < int(args['amount'])):
                print("not enough credit")
                return

            print('=== Found ===')
            
            balanceAt=item['balanceAt']
            transactionAt= item['transactionAt']

            # create new serial port
            # add add transaction here
            # build the cusd string


            ser = initSerial(comPort, 19200)

            print(ser)

            phoneNo = "10560195955"
            #service_amount = "100"
        
            try:
                
                
                #0,ro 0560195955, tapez 1 pour confirmer. Ou tapez 2 pour annuler",68    
                # kwargs will be passed in right through to the read_cusd_logger

                transactionResult = run_Transaction(ser,logger,settings, f'"*{transactionAt}*{phoneNo}*{service_amount}*{simPin}#",15','cusd','confirmer',retry,1,requestId)

                #transactionResult = '0,ro 0560195955, tapez 1 pour confirmer. Ou tapez 2 pour annuler",68'.split(',')

                #transactionResult = '-3, Error'.split(',')


                print(type(transactionResult))


                # rc = 0
                # for r in transactionResult:
                  
                #     print("response from run_balance",rc,r)
                #     rc+= 1

               
                try:
                    if is_integer(transactionResult.errorCode):
                        if int(transactionResult.errorCode) < 0:
                           
                            return(transactionResult)
                        
                except Exception as ex:
                    print('is_integer:' + ex)
                    
                try:
                    
                    if 'confirmer.' in str(transactionResult.message2):

                        print('do conformation')
                        
                        #confirmResult = str(run_Transaction(ser,logger,settings, '"1",15','cusd','succes',0,1,0))

                        pass


                except Exception as ex:
                    print('confirmer:' + ex)



                ff = 0
                #response = str().split()
            except Exception as ex:
                print(ex)
            finally:
                print('-- Port closed --')
                ser.close
            

            print(item)



        except Exception as ex:
            print(ex)



            print(f'Process with {comPort}')

                  
    except Exception as ex:
        print(ex)


    if(comPort == 'null'):
        print('NO COMPORT FOUND')
        return

    result = logger.writelog("Process_transaction 18",f"Transaction amount {args['amount']}")
    
    msg = jsonMessage("C",result)
    #sendRabbit(msg,"D")
    ser = initSerial(comPort,19200)    # <-- here get modem for transaction 

    print(ser)

    #rabbitTransaction(f"Port {ser}",1)


    result = logger.writelog("Process_transaction 17",f"Port {ser}")
    msg = jsonMessage("C",result)
    #sendRabbit(msg,"D")
    
    if(not ser.isOpen):  # if the port is closed transaction will stop here

        result = logger.writelog("Process_transaction",f"Port Closed")
        msg = jsonMessage("C",result)
        #sendRabbit(msg,"D")
        return
    simulate = False

    try:
        with open("C:/System/Data/simulate.pck","rb") as data_file:
            simulate = pickle.load(data_file)
    except:
        pass

    
    
    # try:
    #     with open("C:/System/Data/com_file.pck","wb") as com_file:
    #         pickle.dump(comPort,com_file)  # modem timeout
    
    # except:
    #     pass
    
    response = str(run_balance(ser,logger,settings, f'"*{transactionAt}*{requestId}*{phoneNo}*{service_pin}#",15','cusd','confirmer',simulate,1,0)).split()

    print("After")
    print(type(response))

    rc = 0
    for r in response:
        print("response from run_balance",rc,r)
        rc+= 1
    # print(response.index('No'))
    
    if is_integer(response[0]):

        try:
            if int(response[0]) < 0:

                # print(f"{response[1]} {response[2]} ")
                response_fail.append(response[0])
                response_fail.append(False)
                response_fail.append(f"{response[1]} {response[2]} >> {args[1]} {args[2]}")
                
                return response_fail

            
        except:
            pass


    #rabbitTransaction(f"Modem Response 1 {response}",1)

    result = logger.writelog("Process_transaction 16",f"Modem Response 1 {response}")

    msg = jsonMessage("C",result)
    #sendRabbit(msg,"D")

    transaction_success = False  # default to false


    try:

        if response[5] == 'confirmer.':

            # print("send response")


            # toggle between failure & simulated success with the last arg 1 or 2 

            # here we have our conformation response, 
            sleep(1)


            simulate = '1'

            # confirm with "1"

            # try:
            #     with open("C:/System/Data/com_file.pck","rb") as com_file:
            #         comPort = pickle.load(com_file)
                
            # except:
                
            #     pass
            
            # send the confirm to the network by sending the 1 

            # response here is split on space
            #response = str(run_balance(ser,logger, settings,'"1",15','cusd','succes',simulate,1,str(comPort))).split()

            #rabbitTransaction(f"Modem Response 2 {response}",1)

            # result = logger.writelog("Process_transaction 1",f"Modem Response 2 {response}")
            # msg = jsonMessage("C",result)
            # sendRabbit(msg,"D")

            index_count = 0
            current_credit = 0
            transactionid = 0


                # bringing the string back together
            string_response = ' '.join(map(str,response))

            print(string_response)

            #rabbitTransaction(f"response {string_response}",1)
            
            # string_response
            # +CUSD: 0,"Transfert a l'agent 213551746147 a ete effectue avec succes. Montant STORMCREDIT 100000 Dinar. Numero de l'operation: 210027799535.",68 
            
            result = logger.writelog("Process_transaction 2",f"Response {string_response}")

            msg = jsonMessage("C",result)
            ##sendRabbit(msg,"D")
            
            # rr_count = 0
            # for rr in response:
            #     print("RR",rr_count,rr)
            #     rr_count += 1

            print("="*67)

            for r in response:
                
                print("Response:",index_count,r)


                if r == "minimum":
                    # service responding that the amount requested is below mins
                    transaction_success = False
                    
                    break


                if r == "succes.":
                    # transaction has been accepted
                    print("succes.", index_count)
                    transaction_success = True

                    current_credit == -10
                    if is_integer(str(response[12])):    # check the credit is the type we are expectig
                        current_credit = str(response[12]).replace(",","")

                    transactionid = -10
                    if is_integer(str(response[17]).split(".")[0]):
                        transactionid = str(response[17]).split(".")[0]
                    

                    result = logger.writelog("Process_transaction 3",f"Details {transactionid} | {current_credit}")
                    msg = jsonMessage("C",result)
                    #sendRabbit(msg,"D")

                    break

                # print(r)
                index_count += 1

            bal_after = -1
            try:
                bal_after = int(service_amount) - int(current_credit)
            except:
                pass
            
            # put in 22/03 
            # set the request to a 5 to indicate the network has responded successfully 
            # combat the calling of the transaction again if the final update failed to record
            # this was in response to double transaction in 16/03 where a transaction run twice

            try:

                api_auth.Update_Retry(settings,args[0])
                # query_pre_success = f'''

                # set nocount on 
                # update [dbo].tbl_GATEWAY_FlexyTransactions 
                # set retry = -1,
                # FlexyResponseMessage = 'cusd: transaction réseau réussie'
                # where requestId = {args[0]}

                # '''
                # print(query_pre_success)  

                # engine_pre_success = mssql_engine()
                # conn_pre_success = engine_pre_success.raw_connection()
                # cur_known = conn_pre_success.cursor()
                # cur_known.execute(query_pre_success)
                # cur_known.close()
                # del cur_known

            except Exception as ex:
                print(ex)
                #rabbitTransaction(f"pre_successs {ex}",0)

            response_list = []
            response_list.append(args[0])  #requestId
            response_list.append(transaction_success) # success true of false
            response_list.append(bal_after)  # credit after
            response_list.append(str(int(service_amount))) #credit before
            response_list.append(transactionid)  # nymeric transaction Id
            response_list.append(str(string_response)) # full response message from the network

            for i in response_list:
                print("item:",i)

            print("transaction_success 15:",transaction_success)

            #rabbitTransaction(f"Transaction success {response}",0)

    except Exception as ex:
        print(ex)
        print(" response[5] == 'confirmer.'")
        
        pass

    return response_list

class Conn():
     
    
    engine = mssql_engine()  # imported from database.py
    conn = engine.connect()
    conn1 = engine.raw_connection()
    cursor = conn1.cursor()


class Process_Failure:
    def __init__(self, requestid, retry, settings, transaction):

        self.requestid = requestid
        self.transaction = transaction
        try:
            self.retry = retry
        except Exception as ex:
            print(ex)

    def incRetry(self):

        print("incRetry".center(50,"*"))
       
        return

        updateRetry(self.requestid,self.retry)

    # @timer_decorator
    def update_Transaction_qry_failed(self, message, logger):

        print("update_Transaction_qry_failed".center(50,"*"))

        print(self.requestid)
       
        print(message)
        
        # strip out some junk we don't need
        textToReplace = ["(",")",",","'"]

        try:
            #newMessage = str(message)
            for tr in textToReplace:
                message = str(message).replace(tr,"") 


            print(message)

        except Exception as ex:
            print(ex)
      
        try:
            with open('C:/System/Data/settings.pck', 'rb') as file:
                # Unpickle the data
                data = pickle.load(file)
                host = data['host']
                url = host + f"/Remote/Process_Failure?message={message}&requestId={self.requestid}&transaction={self.transaction}"

            # "http://remote.retailpay.io/Remote/Process_Failure?message=('ro incorrect',)&requestId=6122"
            aadAuth = api_auth.getauthtoken()
            print(aadAuth)
            print(url)
            conn = http.client.HTTPConnection("remote.retailpay.io")
            payload = ''
        
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + aadAuth
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.status_code)

        except Exception as ex:
            print('Remote/Process_Failure: ' + ex)

       
        return
  

        
class Process_Success():
    
    # engine = mssql_engine()  # imported from database.py
    # conn = engine.connect()
    # conn1 = engine.raw_connection()
    # cursor = conn1.cursor()

    def __init__(self, requestid, transactionid, processmode, setings):
        self.transactionid = transactionid
        self.requestid = requestid
        self.processmode = processmode
        self.__orderid = 0

    @timer_decorator
    def GetOrderId(self):
        print(f'get orderid {self.__orderid}')
        return self.__orderid

    # @logger
    @timer_decorator
    def update_Transaction_qry_success(self,requestId,bBefore,bAfter,deviceId,message,refno,logger):

        print("update_Transaction_qry_success".center(30,"*"))


        return

        # print(requestId)
        # print(bBefore)
        # print(bAfter)
        # print(refno)
        # print(message)

        #"[FlexyResponseMessage] = '"+ message.split(':')[1] + "', " +\

        updateTrans_qry = "set nocount on; update [dbo].[tbl_GATEWAY_FlexyTransactions] " + \
            "set [FlexyResponseId] = 0, " + \
                "[FlexyResponseMessage] = '"+ message +"', " +\
                    "[BalanceBefore] = " + bBefore + ", " + \
                        "[BalanceAfter] = " + bAfter + ", " + \
                            "[TransactionStatusId] = 3, " + \
                                "[TransactionTime] = getdate(), " + \
                                    "[RefNumber] = '" + refno + "', " + \
                                        "[DeviceId] = " + deviceId + " " + \
                                            "where [RequestId] = " + str(requestId) +" " +\
                                                "delete from [dbo].[tbl_GATEWAY_FlexyRequests] " + \
                                                    "where [RequestId] = " + str(requestId) +\
                                                        "update [dbo].[tbl_PLATFORM_Devices] " +\
                                                            "set [Balance] = " + bAfter + ", " +\
                                                                "[LastBalance] = getdate() " +\
                                                                    "where [DeviceId] = " + deviceId


        print("*"*75)
        print(updateTrans_qry)
        print("*"*75)

        result_SQL = self.cursor.execute(updateTrans_qry)

        self.cursor.commit()
        
        result = logger.writelog("Process_transaction 14: update_Transaction_qry_success",f"Success FlexyTransactions {result_SQL}")

        msg = jsonMessage("C",result)
        #sendRabbit(msg,"D")

        result = logger.writelog("Process_transaction 13: update_Transaction_qry_success",f"---------------------------------------------")

        msg = jsonMessage("C",result)
        #sendRabbit(msg,"D")

        print(result)

    @timer_decorator
    # @logger
    def process(self, logger):

        print(f"RequestId {self.requestid}")
    
        print(f"TransactionId {self.transactionid}")


        result = logger.writelog("Process_transaction 12",f"process Transaction {self.requestid}")
        msg = jsonMessage("C",result)
        #sendRabbit(msg,"D")

        query = ''   

        # setting nocount seems
        # added 15/04/2023
        # if we get a success from the netork then set the retry value to -1
        # this should prevent the transaqction from being called again if the below fails
        try:    
            updateRetry_Request(self.requestid,4)
        except Exception as ex:
            print(ex)


        try:
            query = "set nocount on; exec bluechip.dbo.sp_PLATFORM_StormPaymentV2 "  + str(self.requestid) + ",1,'" + self.transactionid + "'," + str(self.processmode)
            
            result = logger.writelog("Process_transaction 11",f"process Transaction: {query}")
            msg = jsonMessage("C",result)
            #sendRabbit(msg,"D")



        except Exception as ex:

            result = logger.writelog("Process_transaction",f"{ex}")
            msg = jsonMessage("C",result)
            #sendRabbit(msg,"D")

            print(ex)

        orderNumber = "0"
        print(query)
        try:


            # row = int(self.cursor.execute(sp_qry).fetchone()[0])

            engine = mssql_engine()

            conn1 = engine.raw_connection()

            cursor = conn1.cursor()

            result = cursor.execute(query).fetchall()


            cursor.commit()
      
            cursor.close
            del cursor

            print(result)

            for r in result:
                
                self.__orderid = int(r[0])
                self.stocktransactionId = int(r[1])
                print(f"__orderid {self.__orderid } __stockTransactionId {self.stocktransactionId}")
                
                
            result = logger.writelog("Process_transaction 10",f"process Transaction: Order Number {self.__orderid}, Stock TransactionId {self.stocktransactionId}")

            msg = jsonMessage("C",result)
            #sendRabbit(msg,"D")
           
        except  Exception as e:
            print(e)

class NewTransactions():

    '''this will query for database for any outstanding transactions'''

    def __init__(self,counter, logger,settings,simulate):

        self.counter = counter
        self.logger = logger
        self.settings = settings
        
        #result = self.logger.writelog("NewTransactions",f"({self.counter}) Looking for transactions...")

        #print(result)


        aadAuth = api_auth.getauthtoken()


        print(aadAuth)


        #conn = http.client.HTTPSConnection("loyalty.user.kiwijones.com")

        # pulling from the api

        conn = http.client.HTTPConnection("remote.retailpay.io")
        payload = ''
       
        headers = {
        'Authorization': 'Bearer ' + aadAuth
        }
        
        conn.request("GET", "/Remote/AnyTransactions_ForAccount?accountId=" + settings["AccountId"], payload, headers)
        res = conn.getresponse()
        dataFromApi = res.read()

        # print(data)

        # parts = data.decode("utf-8").split(',')
        

        # Parse JSON string into Python object
        python_Api_Data = json.loads(dataFromApi.decode('utf-8'))

        # Print the Python object
        #print(python_object)
        for dataRow in python_Api_Data:
            phoneNo = dataRow['phoneNumber']
            amount = dataRow['amount']
            requestId = dataRow['requestId']
            retry = dataRow['retry']

            print(phoneNo)
            print(amount)
            print(requestId)
            print(requestId)
            print(retry)

            #return
            try:

                transaction_result =  process_transaction(dataRow,logger=self.logger,settings=settings)

                
                if(int(transaction_result.errorCode) < 0):
                    print("failed")
                    
                    fail = Process_Failure(requestId,0,settings,"rollback")


                    fail.incRetry()    

                    fail.update_Transaction_qry_failed(transaction_result.message1,logger)

                    print(transaction_result.errorCode)

                    print("failed")

                    print(transaction_result.errorCode)
                    print(transaction_result.message1)
                
                if(int(transaction_result.errorCode) >= 0):
                    print("success")
                    success = Process_Success(requestid=requestId)




            except Exception as ex:
                
                print("failed")
                print(ex)
                fail = Process_Failure(requestId,0,settings,"rollback")

        print('NewTransactions: Out' )

            



        # for number in data.decode("utf-8"):
        #     # Print the number multiplied by 2
        #     print(number)

        #print(data.decode("utf-8"))

       
        with open("C:/System/Data/simulate.pck","wb") as data_file:
            pickle.dump(simulate,data_file)

        #print(self.counter)

        # msg = jsonMessage("C",f"({self.counter}) Looking for transactions...")
        #msg = jsonMessage("C",f"{result}")
        #print(msg)
        #sendRabbit(msg,"D")

        # print("result")
        #return
        no_of_Trans = 0


        
        

@Sendmail_Decorator_2
class ProcessException(Exception):
    def __init__(self, message):
        self.message = message
        print(self.message)

        # @logger
        # @Sendmail_Decorator(self.message)
        # def send_email(self):
        #     pass

        # return self.message
    
if __name__ == "__main__":
   

    logger = Logging_File()    

    try:
        with open('C:/System/Data/settings.pck', 'rb') as file:
                # Unpickle the data
                settingsFile = pickle.load(file)
                print(settingsFile)

                try:
                    NewTransactions(45,logger=logger,settings=settingsFile,simulate=False)
                except Exception as ex:
                    print(ex)


    except Exception as ex:
            print('cannot open settings file')
            print(ex)


    # pass
    # # print(response)
        
