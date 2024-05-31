import os
from modem_commands import *
#from database import *
from balance_check import *
from process_transactions import *
from serial_port import scanModems,port_check
from comm_functions import ThreadRabbitReceive
from modem_commands import get_modem_response
from port_scan import ScanThePorts
from os.path import exists
import json
#from class_objects import Setting_File
import shelve
from tkinter import *
import subprocess
import pickle
import pika
import threading

# root = Tk()
# root.title("text gui")
# root.geometry("400x400")

def run():
    subprocess.call(["Modems",'main.py'])


class SetPort():
    
    modem = ""
    port = ""
   
    def __init__(self, inPort, inModemType):

        self.modem = inModemType
        self.port = inPort
        print("set scan", inPort, inModemType)

    
    def balance_check(self):    

        response = ''
       
        ser=port_check(self.port, 19200)

        get_modem_response(ser,'"*570*0000#",15','cusd','Votre','1')

        return response

if __name__=='__main__':

    logger = Logging_File()  

    try:

        f = open("c:/System/Data/Modems.json", "r")
        modems = json.loads(f.read())
        f.close()   
        print(modems)
       
        
        # print(data["server"])
        with open("C:/System/Data/modems.pck","wb") as file:
            pickle.dump(modems,file)
    except Exception as ex:
        print(ex)
    
    try:

        f = open("c:/System/Data/settings.json", "r")
        settings = json.loads(f.read())
        f.close()   
        #print(settings['host'])
        settings['host'] = "http://remote.retailpay.io"  # default url
        if settings['host'] == "dev":
            settings['host'] = "https://localhost:44390"
       
        # print(data["server"])
        with open("C:/System/Data/settings.pck","wb") as file:
            pickle.dump(settings,file)
    except Exception as ex:
        print(ex)
    
    shelve_one = 'C:/System/Data/shelve_one.shlv'

    try:

        if not exists(shelve_one + '.dat'):  
       
            my_shelve = shelve.open(shelve_one, flag='c')    
            my_shelve['Balance'] = True
            my_shelve['Ports'] = True
            my_shelve['Simulate'] = True
            my_shelve['Paused'] = False
            my_shelve["SinglePort"] = ""
            my_shelve["AccountId"] = "13000"
          
            my_shelve.close()
        
    except Exception as ex:
        print(ex)
        
    run_full = True

    process_reset = 500    
    exCounter = 0
    processCounter = process_reset
    bool_process_balance = True
    bool_reset_counter = False

    def callback(ch, method, properties, body):

        decoded =  body.decode()
        print(" [x] Received %r" % decoded)

        if(decoded == "Get"):
            CheckForRequests()
            pass

    # rabbitMg consumer
    def start_consumer():
        #print(__name__)
        print("Thread Rabbit Receive")
        def __init__(self):
            Thread.__init__(self)
        rabbitConf = settings["rabbitMq"].split('|')

        print(rabbitConf)

        userName = rabbitConf[0]
        password = rabbitConf[1]
        host = rabbitConf[2]

        credentials = pika.PlainCredentials(username=userName, password=password)

        parameters = pika.ConnectionParameters(host,
                                            5672,
                                            '/',
                                            credentials)

        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()

        channel.queue_declare(queue=rabbitConf[3])
            
        channel.basic_consume(queue=rabbitConf[3], on_message_callback=callback, auto_ack=True)

        # # print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()  


       
    def CheckForRequests():

        transaction = NewTransactions(processCounter,logger=logger,settings=settings,simulate=False)

        returnCount = transaction.RunTransaction()

        if(int(returnCount) > 0):
                    running_shelve['Balance'] = True

        print("Processed: " + str(returnCount)) 
        

    ScanThePorts(settings,0)
    
    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.daemon = True
    consumer_thread.start()

    #consumer_thread.join()

    while True:

        running_shelve = shelve.open(shelve_one, flag='w')  # open the shelf get the paused param

        #print(running_shelve.__dict__)

        if not running_shelve['Paused']:
            #print(processCounter)
            #print(running_shelve['Balance'])
            if processCounter % 10 == 0:
                running_shelve['Balance'] = True
             
            if running_shelve['Balance']:
                print("Run_Balance")
                try:
                    running_shelve['Balance'] = False
                    with open('C:/System/Data/modems.pck', 'rb') as file:
                        # Unpickle the data
                        modems = pickle.load(file)

                        Threadedbalance(modems)
              
                except Exception as ex:
                    print(ex)

            else:
                
                print(f'Looking for requests: {processCounter}')

                CheckForRequests()

                
        time.sleep(240)

        processCounter -= 1
            
        # if processCounter < 1:
        #     settings = shelve.open("C:/System/Data/shelve_one.shlv",flag='w',writeback=True)
        #     settings['Ports'] = True
        #     settings.close()
        #     processCounter = process_reset
