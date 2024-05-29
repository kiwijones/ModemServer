import smtplib
import pika
import datetime
from threading import Thread
import json
from time import sleep
from class_objects import Setting_File
import shelve
import pickle




class ThreadSendEmail(Thread):
    """
    A threading example
    """

    def __init__(self, to, subject, body):

        print(to)
        print(subject)
        print(body)
        """Initialize the thread"""
        Thread.__init__(self)
        self.to = to
        self.subject = subject
        self.body = body

    def run(self):
        """Run the thread"""
        # amount = random.randint(3, 15)

        sendmail(self.to, self.subject, self.body)
        # print(amount)


class ThreadRabbitReceive(Thread):
    print(__name__)
    print("ThreadRabbitReceive")
    def __init__(self):
        Thread.__init__(self)
         
    # def run(self):
    #         receiveRabbit()

def jsonMessage(type,message):
    print("*"*45)
    print(message)
  
    ''' Default json format to send back to RabbitMQ'''

    try:
        with open("C:/System/Data/rabbit.pck","rb") as data_file:
            server = pickle.load(data_file)

            message = server + ' | ' + message


            print(message)
    except:
        pass


    


    dic = {'type': type,'data': str(message).replace('\n','') }
    jsonString = json.dumps(dic,indent=4)
    return jsonString

def jsonTransaction(type,message, action):
    dic = {'type': type,'data': str(message).replace('\n',''),'action':action }
    jsonString = json.dumps(dic,indent=4)
    return jsonString

def rabbitTransaction(message, action):

    '''this sends to the RabbitMQ that displays on the transaction bar on the dashboard'''    
    msg = jsonTransaction("M",f"{message}",action)


    #sendRabbit(msg,"D")

# def receiveRabbit():
    
        # print('8'*56)
    try:
        host = "92.51.204.82"

        credentials = pika.PlainCredentials('modems', 'v5aWf74MrcDh4Tb')

        parameters = pika.ConnectionParameters(host,
                                            5672,
                                            '/',
                                            credentials)



        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()
        
        server_queue = 'Storm-Modems'

        try:
            with open("C:/System/Data/rabbit.pck","rb") as data_file:
                server = pickle.load(data_file)
                server_queue += '-' + server
        except:
            pass

        print("server_queue",server_queue)   

        channel.queue_declare(queue=server_queue,durable=True)

        def callback(ch, method, properties, body):
            
            strMsg = body.decode()

            # print('callback',strMsg )

            # print('!'*57)

            settings = shelve.open("C:/System/Data/shelve_one.shlv",flag='w',writeback=True)
        
            if strMsg.find("Port") > -1:
                print("Port",strMsg)
                # settings_file.write_setting_file(False,True)
                settings['Ports'] = True

            if strMsg.find("Balance") > -1:
                print("Balance",strMsg)
                # settings_file.write_setting_file(True,False)
                settings['Balance'] = True

            if strMsg.find("Run") > -1:
                print("Pause",strMsg)
                # settings_file.write_setting_file(True,False)
                settings['Paused'] = True

            if strMsg.find("Pause") > -1:
                print("Pause",strMsg)
                # settings_file.write_setting_file(True,False)
                settings['Paused'] = False

            if strMsg.find("Toggle") > -1:


                splitter = strMsg.split('|')

                print(splitter)
                
                if splitter[1] == "On":

                    print("Toggle On")
                  

                    settings["SinglePort"] = str(splitter[2])

                    print(settings["SinglePort"])
                   
                else:
                    print("Toggle off")
                    settings["SinglePort"] = ""




            settings.sync()
            settings.close()

            rabbitTransaction(f"Message received: {body.decode()}",2)


        channel.basic_consume(queue=server_queue, on_message_callback=callback, auto_ack=True)

        # print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except Exception as ex:
        print('callback:', ex)

# def sendRabbit(message, queue):
    '''the function that connects to the RabbitMQ server'''

    try:
        if 'EXCEPTION' in message:
            sendmail("bjones@etlie.com","Modem Server Exception",message)
            sendmail("Technique@proservedz.com","Modem Server Exception",message)
    except Exception as ex:
        print(ex)



    try:


        userName = "vend"
        password = "YHgc7RLiNJaJVmx"
        host = "vpn.etlie.com"
        

        
        # print(message)       
        credentials = pika.PlainCredentials('vend', 'Qaz1234!')

        parameters = pika.ConnectionParameters(host,
                                            5672,
                                            '/',
                                            credentials)



        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()

        # channel.queue_declare(queue='')

        if queue == 'D':
            

            channel.basic_publish(exchange='storm.fanout',
                        
                        routing_key='Storm-Dashboard',
                        # body='Storm --> ' + str(message).rstrip() + ' --> ' + datetime.datetime.now().strftime("%H:%M:%S"))
                        body = str(message).rstrip().replace('[','').replace(']','').replace("'",""))
                      
                        
        else:
            channel.basic_publish(exchange='',
                        routing_key='Vend-Debug',
                        body='Storm --> ' + str(message).rstrip() + ' --> ' + datetime.datetime.now().strftime("%H:%M:%S"))

        
    except Exception as ex:
        print('EX Rabbit')
        print(ex)

def sendmail(recipent, subject, body):
    HOST = "smtp.office365.com"
    SUBJECT = subject
    TO = recipent
    FROM = "support@etlie.com"
    text = body

    BODY = "\r\n".join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "",
        text
    ))

    try:

        server = smtplib.SMTP(HOST, 25)
        server.connect(HOST, 587)

        server.starttls()
        server.login("support@etlie.com", "Fov02511")

        server.sendmail(FROM, [TO], BODY)
        server.quit()
    except Exception as ex:
        print(ex)

def is_integer(n):
    
    '''Takes in a number or number string, returns true if it's an int'''
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()



def string_remove_chars(string):

    ''' when called this will remove these charactors ["(",")",",","'","\""] from the string being passed in'''

    textToReplace = ["(",")",",","'","\""]

    try:
            #newMessage = str(message)
            for tr in textToReplace:
                string = str(string).replace(tr,"") 


            print(string)

    except Exception as ex:
            print(ex)

    return string

def sendRabbit(message, queue):
    '''the function that connects to the RabbitMQ server'''
    
    try:
        if 'EXCEPTION' in message:
            sendmail("bjones@etlie.com","Modem Server Exception",message)
            #sendmail("Technique@proservedz.com","Modem Server Exception",message)
    except Exception as ex:
        print(ex)

    try:

        userName = "vend"
        password = "YHgc7RLiNJaJVmx"
        host = "92.51.204.82"
        
        # print(message)       
        credentials = pika.PlainCredentials(username=userName, password=password)

        parameters = pika.ConnectionParameters(host,
                                            5672,
                                            '/',
                                            credentials)

        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()

        # channel.queue_declare(queue='')

        if queue == 'D':
            

            channel.basic_publish(exchange='storm.fanout',
                        
                        routing_key='Storm-Dashboard',
                        # body='Storm --> ' + str(message).rstrip() + ' --> ' + datetime.datetime.now().strftime("%H:%M:%S"))
                        body = str(message).rstrip().replace('[','').replace(']','').replace("'",""))
                      
                        
        else:
            channel.basic_publish(exchange='',
                        routing_key='Vend-Debug',
                        body='Storm --> ' + str(message).rstrip() + ' --> ' + datetime.datetime.now().strftime("%H:%M:%S"))

        
    except Exception as ex:
        print('EX Rabbit')
        print(ex)

if __name__ == "__main__":

    print("__main__")
    #receiveRabbit()    


    # shelve_one = 'C:/System/Data/shelve_one.shlv'

    # running_shelve = shelve.open(shelve_one, flag='w')  # open the shelf get the paused param

    # print(list(running_shelve.items()))
    # print(running_shelve.__dict__)


    # shelve_one["SinglePort"] = "COM45"

    # print(list(running_shelve.items()))
    
    msg = jsonMessage('D','Test')  # send the queue to rabbit
    sendRabbit(msg.replace('\n',''),"D")
