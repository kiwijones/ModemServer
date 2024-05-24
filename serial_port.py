'''Seriall port functions '''
from colorama import Fore
import serial
from database import modemKnowToSystem
# from modem_commands import get_modem_response

def initSerial(comPort,baudrate):

    print(comPort,baudrate)
    # print('Serial port initialize...', end='')

    ser = serial.Serial()
    ser.port = comPort
    ser.baudrate = baudrate
    ser.timeout = 0.1  # timeout block read
    ser.writeTimeout = 0.1
    ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
    ser.parity = serial.PARITY_NONE  # set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE  # number of stop bits
    ser.xonxoff = False  # disable software flow control
    ser.rtscts = False  # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control
    try:
        print(ser)
        ser.open()

    except:
        print("Com port not found")
        

        
    return ser
def scanModems():
    available = []
    for i in range(256):
        try:
            s = serial.Serial('COM'+str(i))
            #print(s)
            available.append( (s.portstr))
            s.close()   # explicit close 'cause of delayed GC in java

        except serial.SerialException:
            pass


    return(available)


def port_check(comPort,baudrate):
    # print(comPort,baudrate)
    return initSerial(comPort,baudrate)
