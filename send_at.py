# def write_to(dd, cmd, waitFor):

#     at_bytes = b'at+'

#     at_string = cmd + '\r'

#     comma = at_bytes + at_string.encode('utf-8')

#     print(comma)

#     dd.write(comma)

#     if waitFor == 1:

#         # print(cmd)
#         response = read_from
#         # print(response)

#         if response == "OK":
#             if (dd.in_waiting):

#                 response == read_from
#                 print('**')
#                 print(response)


def ussd_cmd(ser,cmd,mode):


    print(cmd)

    ser.reset_input_buffer()

    at_bytes = b'at+cusd=' 

    at_string = mode + "," + cmd + '\r'

    cmd_to_send = at_bytes + at_string.encode('utf-8')

    print(cmd_to_send)

    ser.write(cmd_to_send)


    # wait for the modem to respond
    while True:
       
        if(ser.in_waiting):  
            data_from_modem = read_buffer(ser) # reat the data

            print(data_from_modem)

            if data_from_modem.find('OK') > -1:
                return 'OK'


            if data_from_modem.find('+CME') > -1:
                break

            # elif data_from_modem.find('service!') > 0:
            #     return 'service'
            # elif data_from_modem.find('PIN') > 0:
            #     return 'pin'


def wait_for_ussd_response(ser, calling_service, calling_number):
     while True:
        if(ser.in_waiting):  

            data_from_modem = read_buffer(ser) # read the data
            
            print("[" + str(calling_number) + "]:",  data_from_modem)


            if data_from_modem.find(': 4') > 0:
                   return 'NOTOK'

            if data_from_modem == "+CUSD: 4":
                return 'NOTOK'


            if len(data_from_modem) == 0:
                return 'NOTOK'
            
            
            if data_from_modem.find('OK') > -1:
                return 'OK'

            if(calling_service == 'b'):  # balance checks
                if data_from_modem.find('service') > 0:
                    return 'service|' + str(data_from_modem)
                elif data_from_modem.find('Daily Report') > 0:
                    return 'report|' + str(data_from_modem)
                
            if(calling_service == 'c'):  # credit processing
                if data_from_modem.find('service!') > 0:
                   return 'service|' + str(data_from_modem)
                elif data_from_modem.find('Amount') > 0:
                    return 'Amount|' + str(data_from_modem)
                elif data_from_modem.find('sure') > 0:
                    return 'Sure|' + str(data_from_modem) 
                elif data_from_modem.find('Sorry') > 0:
                    return 'Sorry|' + str(data_from_modem)
                elif data_from_modem.find('Private') > 0:
                    return 'Private|' + str(data_from_modem)
                elif data_from_modem.find('top-up') > 0:
                    return 'top-up|' + str(data_from_modem)
                elif data_from_modem.find('Dear') > 0:
                    return 'Dear|' + str(data_from_modem)
                
            if data_from_modem.find('PIN') > 0:  # this is used in both
                return 'pin|' + str(data_from_modem)
            
            if data_from_modem.find('stock balance') > 0:
                return data_from_modem


def read_buffer(ser, terminator='\n'):

    print('reading {}...'.format(ser.name))

    resp = ''
    while not (resp.endswith(terminator) or resp.endswith('\r')):  # If the string is not terminated
        tmp = ser.readline().decode('utf-8')   # Read and store in a temp variable
        if not tmp:
            return resp  # timeout occured
        resp += tmp
    return resp