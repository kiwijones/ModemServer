
import os
import json
from datetime import datetime


class Logging_File:
    logpath = "c:\\EasonLog\\StormModems"
    
    def __init__(self):
        
        if not os.path.exists(self.logpath):
           os.makedirs(self.logpath)

        print(self.logpath)

    def writelog(self,action,message):

        logfile = self.logpath + "\\StormModems_" + datetime.today().strftime('%Y-%m-%d') + ".log"

        if os.path.isfile(logfile):
            # print("there")
            pass
        else:
            fileToWrite = open(logfile,"w")
            fileToWrite.close




        # self.logpath + "\\StormModems_" + datetime.today().strftime('%Y-%m-%d') + ".log"

        # if os.path.isfile(self.logfile):
        #     # print("there")
        #     pass
        # else:
        #     fileToWrite = open(self.logfile,"w")
        #     fileToWrite.close
        
        
        fileToWrite = open(logfile,"a")
        
        toFile = f"{datetime.today().strftime('%H:%M:%S')}> {action}: {message} \n"
        
        # if "new" in message:
        #     Sendmail_Decorator('Process Exception')


        # for r in range(0,10):
           
        fileToWrite.writelines(toFile)

        fileToWrite.close()

        return toFile


    
class Setting_File:

    def __init__(self,filename):
        self.filename = filename

        
       
    def set_setting_file(self):
        settings_file = os.path.exists(self.filename)
        
        if settings_file == False:
        
            dictionary = {"Run_Balance": True,"Run_PortScan": False}

            json_object = json.dumps(dictionary, indent=4)
            with open(self.filename, "w") as outfile:
                outfile.write(json_object)


    def read_setting_file(self):

        print(self.filename)
        with open(self.filename, 'r') as openfile:
            return json.load(openfile)

    def write_setting_file(self,balance_check, port_scan):
        dictionary = {"Run_Balance": balance_check,"Run_PortScan": port_scan}
        json_object = json.dumps(dictionary, indent=4)
        with open(self.filename, "w") as outfile:
                outfile.write(json_object)

class Live_File:

    def __init__(self,filename):
        self.filename = filename

        
       
    def set_Live_file(self):
        settings_file = os.path.exists(self.filename)
        
        if settings_file == False:
        
            dictionary = {"Live": True}

            json_object = json.dumps(dictionary, indent=4)
            with open(self.filename, "w") as outfile:
                outfile.write(json_object)


    def read_Live_file(self):

        print(self.filename)
        with open(self.filename, 'r') as openfile:
            return json.load(openfile)

    def write_setting_file(self,set_live):
        
        dictionary = {"Live": set_live}
        json_object = json.dumps(dictionary, indent=4)
        with open(self.filename, "w") as outfile:
                outfile.write(json_object)

class TransactionResponse:
    def __init__(self,errorCode, message1, message2,message3):
        self.errorCode = errorCode
        self.message1 = message1,
        self.message2 = message2,
        self.message3 = message3,

    def returnResponse(self):
        return(self)


if __name__ == "__main__":

    logger = Logging_File()

    response =  logger.writelog("ACTION","this is test")
    
