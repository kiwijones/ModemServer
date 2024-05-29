
import pickle
from threading import Thread
from time import sleep
from colorama import Fore, Back, Style, init
init() # colorama
from database import modemKnowToSystem, set_active_comport
from modem_commands import get_modem_response
from serial_port import initSerial, scanModems
from class_objects import Logging_File
#from comm_functions import sendRabbit,jsonMessage
from comm_functions import jsonMessage
import random
import shelve
from api_auth import ModemStartup
import serial.tools.list_ports
import array as portArray


def taskPorts(comPort,que,logger, settings, report):

    print(f"started {comPort}")

    ser = initSerial(comPort,19200)

    print('\033[39m')
    # print('\039[39m' + ser)


    #return
    # result = logger.writelog("looking for Serial",f"{comPort}")
    #msg = jsonMessage('D',f"looking for Serial (IMEI): {comPort}")  # send the queue to rabbit
    #sendRabbit(msg.replace('\n',''),"D")


    # get the modem serial number
    serialResponse = get_modem_response(ser,'at+CGSN','init','WAITFOR')  # serial

    #serialResponse = get_modem_response(ser,'at&f','init','WAITFOR')  # serial

    print('>'*50)
    
    print('\033[32m' + "serialResponse",serialResponse)

    print('\033[39m')

    try:
        if serialResponse.isdigit():

            try:
                if(int(report) > 0):
                    print(" Found Modem ".center(50,"*"))
                    print((str(comPort) + " " + str(serialResponse)).center(50," "))
                    print("".center(50,"*"))
                    return

            except Exception as ex:
                pass
            # next step

            # result = logger.writelog("looking for IMSI",f"{serialResponse}")


            #msg = jsonMessage('D',f"looking for IMSI: {serialResponse}") # send the queue to rabbit
            #sendRabbit(msg.replace('\n',''),"D")

            print("Now look for IMSI")
            # here we have found a serialNo, try and get IMSI

            ismiResponse = get_modem_response(ser,'at+CIMI','init','WAITFOR')  # serial
            
            # return
            if ismiResponse.find("CME") == -1:   # 
                
                # result = logger.writelog("Found IMSI",f"{ismiResponse}")
                #msg = jsonMessage('D',f"Found IMSI: {ismiResponse}")  # send the queue to rabbit
                #sendRabbit(msg.replace('\n',''),"D")

                print("ismiResponse",ismiResponse)
                
                # at this point we have a functional modem
                # here we will report to the server

                # look through the modems file to pick out the modem type & simPin

                with open('C:/System/Data/modems.pck', 'rb') as file:
                    # Unpickle the modem data
                    modemFile = pickle.load(file)

                simType = -1
                simPin = ""
                for modem in modemFile:
                     if modem["IMSI"] == ismiResponse:
                        simType = modem["type"]
                        simPin = modem["simPin"]


                print('\033[32m'  + "MODEM FOUND: "  + comPort + " --> " + ismiResponse + " --> " + simPin)
                
                try:
                    # this will update insert the modem details on the server
                    ModemStartup(settings['AccountId'],comPort,1,serialResponse, ismiResponse, 0,settings['Server'],simType,simPin, settings=settings)
                except Exception as ex:
                    print("SendLastSeen: " + ex)
                
                print('\033[39m' + "")
                
            else:

                # result = logger.writelog("CME Error... ",f"{comPort} {serialResponse}")
                #msg = jsonMessage('D',f"CME Error: {comPort} {serialResponse}")  # send the queue to rabbit
                #sendRabbit(msg,"D")

                print("CME Error... ", serialResponse)

                print(f"Setting serial {serialResponse}")

                set_active_comport(serialResponse,'',comPort,-1,'-1-1-1-1','CME Error...')
            
        else:
            print("serialResponse not dgit")
            #msg = jsonMessage('D',f"serialResponse not digit: {comPort}")  # send the queue to rabbit
            #sendRabbit(msg,"D")
            # print(Fore.WHITE)
    except Exception as ex:
        print(ex)
        print("Modem not on port")
        #SendLastSeen(settings['AccountId'],comPort,0,"Not Found")



def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return(ports)
    # for port, desc, hwid in sorted(ports):
    #     print(f"Port: {port}")
    #     print(f"Description: {desc}")
    #     print(f"HWID: {hwid}\n")


def ThreadPorts(settings, report):

    threads = []  # thread list
    que = []  #que list, this object is passed into the threaded task where it gets appended to


    # first loop through all ports on the server
    print("Report: " + str(report))
    logger = Logging_File()


    # return the list of serial ports
    portList = list_serial_ports()

    #create an array to hold found ports
    foundPorts = []
    for port, desc, hwid in sorted(portList):
     
        foundPorts.append(port + "," + desc)

    
    # loop through founds
   
    try:
        if len(foundPorts) > 0:

            for comPort in foundPorts:
            
                portSplit = comPort.split(',')
                
            
                if "Secondary" in portSplit[1]:
                    print(portSplit[0])
                    print(portSplit[1])
                    taskPorts(portSplit[0],que,logger,settings, report)


    except Exception as ex:
        print(ex)

def ScanThePorts(settings,reports):

    #settings['Ports'] = False

    ThreadPorts(settings, reports)

def ScanThePorts1():

    

    ThreadPorts()


if __name__ == "__main__":
    

    # shelve_one = 'C:/System/Data/shelve_one.shlv'

    # running_shelve = shelve.open(shelve_one, flag='w')  

    try:
         
        with open('C:/System/Data/settings.pck', 'rb') as file:
            # Unpickle the data
            settings = pickle.load(file)

            #client_secret = data['client_secret']
            # the 0 here is modem reporting, is set to 1 the script will report modem com and IMSI but not 
            # update database

            ScanThePorts(settings,0)

    except Exception as ex:
            print('cannot open settings file')
            print(ex)


   