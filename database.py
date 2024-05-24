
import pyodbc
import sqlalchemy as sal
import pandas as pd
from sqlalchemy import create_engine
#from comm_functions import sendRabbit,jsonMessage
from comm_functions import jsonMessage

# def mssql_engine(user="appAccess", password="app_9001", host="89.204.219.225,11433", db="etl"):
# def mssql_engine(user="appAccess", password="app_9001", host="192.168.5.45", db="etl"):
def mssql_engine(user="appAccess", password="(*qaz1234*)", host="192.168.15.112", db="etl"):
    engine = sal.create_engine(
        f'mssql+pyodbc://{user}:{password}@{host}/{db}?driver=SQL+Server')

    #print(engine)
    return engine

# def mssql_conn():
#     server = '89.204.219.225,11433' 
#     database = 'etl' 
#     username = 'appAccess' 
#     password = 'app_9001' 

def mssql_conn():
    server = '192.168.15.112' 
    database = 'etl' 
    username = 'appAccess' 
    password = '(*qaz1234*)' 


# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=no;UID='+username+';PWD='+ password)
    return cnxn

def update_balance(balance):
    query = "update [dbo].[tbl_PLATFORM_Devices] set balance = " + \
    balance + ", lastBalance = getdate() where deviceId = 2"

    print(query)

    engine = mssql_engine()

    conn = engine.connect()

   

# print(engine.table_names())

    result = engine.execute(query)

    # for row in result:
    #     print(row)

    result.close()




def update_success_Transaction(requestId, refNumber, responseMessage):
    query = "update [dbo].[tbl_GATEWAY_FlexyTransactions] " + \
        "set RefNumber = '" + str(refNumber) + "', " + \
            "TransactionTime = getdate()," + \
                "FlexyResponseMessage = '" + str(responseMessage) + "' " + \
                    "where [RequestId] = " + str(requestId) + " " + \
                        "select @@rowcount"



    engine = mssql_engine()

    conn = engine.connect()

    result = engine.execute(query)



    return query

def get_transaction_query_1(modemId):
    
    query = "set nocount on;  update FT " + \
    "set FT.[TransactionStatusId] = 2 " +\
    "from [dbo].[tbl_GATEWAY_FlexyTransactions] FT " + \
    "join  [tbl_GATEWAY_FlexyRequests] FR on fr.RequestID = ft.RequestId " + \
    "WHERE (FR.[ModemID] = " + str(modemId) +" AND FR.[Status] = 0) " + \
        "select @@rowcount as 'RowCount'"

    return query


def get_transaction_query_2(modemId):
    
    # query = "update FT " + \
    # "set FT.[TransactionStatusId] = 2 " +\
    # "from [dbo].[tbl_GATEWAY_FlexyTransactions] FT " + \
    # "join  [tbl_GATEWAY_FlexyRequests] FR on fr.RequestID = ft.RequestId " + \
    # "WHERE (FR.[ModemID] = 2 AND FR.[Status] = 0)" + \
    query =  "SELECT fr.[RequestID], fr.[PhoneNumber], fr.[Amount], fr.[Batch]  FROM [tbl_GATEWAY_FlexyRequests] FR " + \
    "join [dbo].[tbl_GATEWAY_FlexyTransactions] FT on fr.RequestID = ft.RequestId " + \
    "WHERE (fr.[ModemID] = " + modemId + " AND fr.[Status] = 0 and ft.TransactionStatusId = 2) " +\
    "ORDER BY fr.[Inserted] "

    return query


def get_TransactionId_Qry(requestId):

    query = "select at.[Guid] from [etl].[dbo].[tbl_GATEWAY_FlexyTransactions] ft " + \
        "join [etl].[dbo].[tbl_PLATFORM_Api_Transaction] at on ft.[TransactionId] = at.[TransactionId] " + \
            "where ft.[RequestId] = "  + str(requestId)

    
    return query

def update_Transaction_qry(guid,other, requestId):

    query = "set nocount on; update [dbo].[tbl_GATEWAY_FlexyTransactions] " + \
        "set [FlexyResponseId] = 0 ,[RefNumber] = '" + guid + "', " + \
            "[FlexyResponseMessage] = '"+ other + "', " +\
                "[TransactionStatusId] = 3 " + \
                    "where [RequestId] = " + str(requestId) 


    return query

# def delete_Request_qry(requestId):
    

def get_sp_PLATFORM_StormPayment(requestId,other, processMode):

    query = ''   

    # setting nocount seems
    try:
        query = "set nocount on; exec bluechip.dbo.sp_PLATFORM_StormPayment "  + str(requestId) + ",1,'" + other + "'," + str(processMode)
    
    except Exception as ex:
        print(ex)

    return query

def Process_Success_Transaction(requestId, other):




    
    print('Process_Success_Transaction')

    processMode = 0



    guid_Query =  get_TransactionId_Qry(requestId)

    engine = mssql_engine()

    conn = engine.connect()

    conn1 = engine.raw_connection()

    result = engine.execute(guid_Query)



    # print(result)

    guid = ''
    for row in result:
        
        guid = row[0]
        print('Guid: ' + str(guid))

   
    # result.close()

    print(str(other))

    print(str(requestId))

    cursor = conn1.cursor()

    updateTrans_qry = update_Transaction_qry(guid,str(other),requestId)

    print(updateTrans_qry)
    
    result = cursor.execute(updateTrans_qry)

    cursor.commit()

    print(result)

    sp_qry = get_sp_PLATFORM_StormPayment(requestId, other, processMode)

    cursor = conn1.cursor()
    
    orderNumber = "0"
   
    try:
        row = cursor.execute(sp_qry).fetchone()
        
        while row:

            orderNumber = str(row[0])

            print('OrderNo: ' + str(row[0]))
            row = cursor.fetchone()
    except  Exception as e:
        print(e)

    cursor.commit()
    cursor.close()
    



    print(type(orderNumber))

    #print(str(result[0]))
    return orderNumber
   
#########################


def get_device_details_msisdn(msisdn):
    



    query = "set nocount on;  select devicedetail from [dbo].[tbl_platform_devices]  " + \
        "where devicereference = '"  + msisdn + "' and active = 1" 
    return query



def modemKnowToSystem(imsi):

    query = f"set nocount on; select * from [Bluechip].[dbo].[tbl_MANAGEMENT_StormSims] where [IMSI] = '{imsi}'"
    print(query)

    engine = mssql_engine()  # imported from database.py
    conn = engine.raw_connection()

    cur_known = conn.cursor()

    
    #return engine.execute(query)


    

    result = cur_known.execute(query).fetchall()

   
    print(result)
    # for  r in result:
    #     return r

    # # print(result[0],)

    return result



def set_active_comport(serialNo, IMSI,comPort, zone, simpin,description,server):

    print(f"Updating {serialNo} {IMSI} {comPort} {zone} {simpin} {description} {server}")

    query = "set nocount on; exec [dbo].[sp_PLATFORM_StormModem] " +\
                "'" + str(serialNo) + "'," +\
                    "'" + str(IMSI) + "'," +\
                        "'" + str(comPort) + "'," +\
                            str(zone) + "," +\
                                "'" + str(simpin) +"'," +\
                                    "'" + str(description) + "', " +\
                                        "'" + str(server) + "' "





    msg = jsonMessage('C',f"{query}")  # send the queue to rabbit

    sendRabbit(msg,"D")


    try:

        engine = mssql_engine()

        conn1 = engine.raw_connection()

        cursor = conn1.cursor()

        result = cursor.execute(query)

        cursor.commit()
      

        print(result)


    except Exception as ex:
        print(ex)



    # return query
