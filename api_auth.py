
import datetime
import requests
import json
import pickle
from datetime import datetime
from comm_functions import jsonMessage,sendRabbit

def getauthtoken():

    getAuth = False

    int_unix_timestamp = int(datetime.now().timestamp())

    #print (int_unix_timestamp)

    # unixTime = datetime(datetime.UTC)

    # get the previous token expiry
    
    with open('AADAuth.pickle', 'rb') as f:

        azure_Auth_Load = pickle.load(f)

        print(int(azure_Auth_Load["expires_in"]) / 9.7)
        
        # this will compare the token expity if less that 300 then get a new one
        if (int(azure_Auth_Load["expires_on"]) -int_unix_timestamp) < int(azure_Auth_Load["expires_in"]) / 9.7:
            getAuth = True
        else:
            print("Return with saved pickle")
            return azure_Auth_Load["access_token"]
        
    if(getAuth):   
        client_secret = ""

        # get client secret from the setting pickle
        try:
         
            with open('C:/System/Data/settings.pck', 'rb') as file:
                # Unpickle the data
                data = pickle.load(file)

                client_secret = data['client_secret']

        except Exception as ex:
            print(ex)

        print("Get Auth")
        url = "https://login.microsoftonline.com/a0817e83-5773-4b60-bf40-981a75615789/oauth2/token"

        payload = {'grant_type': 'client_credentials',
        'client_id': '9074d7b4-d176-476c-97f4-3b0f26125993',
        'Resource': 'api://9074d7b4-d176-476c-97f4-3b0f26125993',
        'client_secret': client_secret}
        files=[

        ]
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'fpc=AoXpJZwmCipLlRz7yNa2muuEzPGGAQAAAAIfyd0OAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
        }

        response = requests.request("GET", url, headers=headers, data=payload, files=files)

        azure_Auth = json.loads(response.text)

        with open('AADAuth.pickle', 'wb') as f:
            pickle.dump(azure_Auth, f)
   
    try:
        with open('AADAuth.pickle', 'rb') as f:
            print("getting latest pickle")
            azure_Auth_Load = pickle.load(f)
            
    except Exception as e:
       
        print(e)
        print("AADAuth not found")

    return azure_Auth_Load["access_token"]

def ModemBalance(accountId,comPort,isActive,imei, balance, logger, settings):
    
    authtoken = getauthtoken()

    #print(authtoken)

    try:
    

        with open('C:/System/Data/settings.pck', 'rb') as file:
            # Unpickle the data
            data = pickle.load(file)

            host = data['host']

        url = host + "/Remote/Update_AccountModemBalance"

        print(url)
        #print(authtoken)

        formatBalance = balance.replace("'","")

        payload = json.dumps({
        "accountId": accountId,
        "comPort": comPort,
        "balance": formatBalance,
        "isActive": isActive,
        "imei": imei

        })
        
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + authtoken
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        msg = jsonMessage( 'C',f"{ comPort},{imei},{formatBalance}", 'ModemBalance', settings=settings)  # send the queue to rabbit

        sendRabbit(msg,"D")    
        # print(response.status_code)

        # print(payload)

        return

    except Exception as ex:
            
            print(ex)
            return

def SendLastSeen(accountId,comPort,isActive,imei, balance):
    
    authtoken = getauthtoken()


    print(authtoken)

    try:
    

        with open('C:/System/Data/settings.pck', 'rb') as file:
            # Unpickle the data
            data = pickle.load(file)

            host = data['host']

        url = host + "/Remote/Update_AccountModemLastSeen"

        print(url)
        #print(authtoken)

        payload = json.dumps({
        "accountId": accountId,
        "comPort": comPort,
        "balance": balance.replace("'",""),
        "isActive": isActive,
        "imei": imei

        })

        
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + authtoken
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.status_code)

        print(payload)

        return

    except Exception as ex:
            
            print(ex)
            return

def ModemStartup(accountId,comPort,isActive,imsi,imei,  balance, server, simType, simPin, settings ):

    # only called on port_scan uopn startup
    
    authtoken = getauthtoken()

    try:
        
        simTypeId = 2 # default set to aux

        if simType == 'primary':
            simTypeId = 1


        with open('C:/System/Data/settings.pck', 'rb') as file:
            # Unpickle the data
            data = pickle.load(file)

            host = data['host']


            url = host + "/Remote/Update_AccountStartUp"

            #print(url)
            #print(authtoken)

            payload = json.dumps({
            "accountId": accountId,
            "comPort": comPort,
            "balance": "0",
            "isActive": isActive,
            "imsi": imsi,
            "imei": imei,
            "simType": simTypeId,
            "server": server,
            "simPin": simPin
            })

            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + authtoken
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            try:
                msg = jsonMessage( 'C',f"{ comPort},{imei},{simType}", 'ModemStartup', settings=settings)  # send the queue to rabbit
                sendRabbit(msg,"D")
            except:
                pass
            
            print(response.status_code)
            print(payload)

            return

    except Exception as ex:
            
            print(ex)
            return


    if __name__ == "__main__":
        #print("hello")

        # partner azure
        print(getauthtoken())

def GetComportForIMEI(imei, settings, logger):
    
    logger.writelog("GetComportForIMEI",imei)
    authtoken = getauthtoken()
    
    print(authtoken)

    host = settings['host']
    accountId = settings['AccountId']

    url = host + "/Remote/Get_ComportForIMSI?accountId=" + accountId +"&imsi=" + imei

    print(url)

    payload = {}
    headers = {
    'Authorization': 'Bearer ' + authtoken
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    logger.writelog("GetComportForIMEI",response.text)

    return(response.text)

def Get_ComportForProduct(settings, productId, amount, simTypeId, logger):

        
    try:
            msg = jsonMessage( 'C',f"{productId},{amount},{simTypeId}", 'Get_ComportForProduct', settings=settings)  # send the queue to rabbit

            sendRabbit(msg,"D")
    except:
            pass
    
    logger.writelog("Get_ComportForProduct",str(productId))
    authtoken = getauthtoken()
    host = settings['host']
    accountId = settings['AccountId']

    url = host + f"/Remote/Get_ComportForProduct?accountId={accountId}&productId={productId}&amount={amount}&simTypeId={simTypeId}"

    payload = {}
    headers = {
    'Authorization': 'Bearer ' + authtoken
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.status_code)

    logger.writelog("Get_ComportForProduct",str(response.text))

    return(response.text)
   
def Update_Retry_RequestId(settings,requestId, value):
    
    try:
            msg = jsonMessage( 'C',f"{requestId},{value}", 'Update_Retry_RequestId', settings=settings)  # send the queue to rabbit

            sendRabbit(msg,"D")
    except:
            pass 

    authtoken = getauthtoken()

    host = settings['host']
   
    try:
        url = host + "/Remote/Update_Retry_RequestId?requestId=" + str(requestId) + "&value=" + str(value)
   
    except Exception as ex:
        print(ex)
    

    payload = {}
    headers = {
    'Authorization': 'Bearer ' + authtoken
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.status_code)
    return(response.status_code)

def Update_Retry_TransactionId(settings,transactionId, retry):
    
    try:
        msg = jsonMessage( 'C',f"{transactionId},{retry}", 'Update_Retry_TransactionId', settings=settings)  # send the queue to rabbit

        sendRabbit(msg,"D")

    except:
        pass 
     
    authtoken = getauthtoken()

    host = settings['host']
   
    url = host + "/Remote/Update_Retry_TransactionId?transactionId=" + str(transactionId) + "&retry=" + str(retry)

    payload = {}
    headers = {
    'Authorization': 'Bearer ' + authtoken
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    return(response.text)

def Update_Process_failed(settings, message, requestId, retry):
   
    try:

        transaction = 'commit'

        authtoken = getauthtoken()
        
        host = settings['host']
        url = host + "/Remote/Process_Failure?message=" + str(message) + "&requestId=" + str(requestId) +"&transaction=" + str(transaction)

        payload = {}
        files={}
        headers = {
        'Authorization': 'Bearer ' + authtoken
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text)
    except Exception as ex:
        print(ex)

def Update_Process_Retry(settings, message, requestId):
   
    try:

        transaction = 'commit'

        authtoken = getauthtoken()
        
        host = settings['host']
        url = host + "/Remote/Process_Retry?message=" + str(message) + "&requestId=" + str(requestId) +"&transaction=" + str(transaction)

        payload = {}
        files={}
        headers = {
        'Authorization': 'Bearer ' + authtoken
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text)
    except Exception as ex:
        print(ex)

def Update_Process_Success(settings, message,bBefore,bAfter,refno,deviceId,requestId,logger):
   
    try:
        logger.writelog("Update_Process_Success",str(message))

        authtoken = getauthtoken()
                
        host = settings['host']
        
        transaction = "commit"

        url = host + "/Remote/Process_Success?message=" + str(message) + "&bBefore="+ str(bBefore) + "&bAfter=" + str(bAfter)        + "&refno="+ str(refno) + "&deviceId="+ str(deviceId) +"&requestId=" + str(requestId) + "&transaction=" + transaction
        print(url)
        payload = {}
        headers = {
        'Authorization': 'Bearer ' + authtoken
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        #logger.writelog("Update_Process_Success",str(response.text))
    except Exception as ex:
        print(ex)

def AnyTransactions_ForAccount(settings):
    try:

        # msg = jsonMessage('C',f"{"Ping"}")  # send the queue to rabbit

        # sendRabbit("AnyTransactions_ForAccount",msg,"D", settings=settings)   

        try:
            msg = jsonMessage( 'C',f"Ping", 'AnyTransactions_ForAccount', settings=settings)  # send the queue to rabbit

            sendRabbit(msg,"D")
        except:
            pass 

        authtoken = getauthtoken()
                
        host = settings['host']

        url = host + "/Remote/AnyTransactions_ForAccount?accountId=" + str(settings["AccountId"]) + "&retry=" + str(settings["retry"])

        payload = {}
        headers = {
        'Authorization': 'Bearer ' + authtoken
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.status_code)
        return(response.text)
    
    except Exception as ex:
        print(ex)


