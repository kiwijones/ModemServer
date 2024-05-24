import threading
import time
from colorama import *
#from comm_functions import sendRabbit,jsonMessage
from comm_functions import jsonMessage
from datetime import datetime
import smtplib
from queue import Queue
from comm_functions import sendmail,ThreadSendEmail
from threading import Thread



# class ThreadSendEmail(Thread):
#     """
#     A threading example
#     """

#     def __init__(self, to, subject, body):
#         """Initialize the thread"""
#         Thread.__init__(self)
#         self.to = to
#         self.subject = subject
#         self.body = body

#     def run(self):
#         """Run the thread"""
#         # amount = random.randint(3, 15)

#         sendmail(self.to, self.subject, self.body)
#         # print(amount)

def threadedQueue(f, daemon=False):
   

    def wrapped_f(q, *args, **kwargs):
        '''this function calls the decorated function and puts the 
        result in a queue'''
        ret = f(*args, **kwargs)
        q.put(ret)

    def wrap(*args, **kwargs):
        '''this is the function returned from the decorator. It fires off
        wrapped_f in a new thread and returns the thread object with
        the result queue attached'''

        q = Queue()

        t = threading.Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        t.daemon = daemon
        t.start()
        t.result_queue = q        
        return t

    return wrap

def timer_decorator(function):
    def wrapper(*args,**kwargs):
        start = time.time()
        # print(f"Starting function {function.__name__} at time {start}")
        value = function(*args, **kwargs)
        end = time.time()
       
        # print(Fore.BLUE)

        # msg = jsonMessage("C",f"{function.__name__} {end - start}")
        # print(msg)
        # sendRabbit(msg,"D")

        print(f"{function.__name__} {end - start}")
        # print(Fore.WHITE)
        return value
       
    return wrapper

def logger (function):
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)    
        with open("function_log.log", mode='a') as f:
            f.write(f"{datetime.now()} Function name {function.__name__} with args '{args}'\n")

        return value
        
    return wrapper

@timer_decorator
def new_email_thread(to, subject, body):

        my_thread = ThreadSendEmail(to, subject, body)
        my_thread.start()


class WarehouseDecorator:
    def __init__(self, material):
        self.material = material

    def __call__(self, own_function):
        def internal_wrapper(*args, **kwargs):
            print('<strong>*</strong> Wrapping items from {} with {}'.format(own_function.__name__, self.material))
            own_function(*args, **kwargs)
            print()
        return internal_wrapper


def Sendmail_Decorator_2(function):
    def wrapper(*args,**kwargs):

        print(*args)

        start = time.time()
        print(f"starting function {function.__name__} {start}")
        value = function(*args, **kwargs)
        new_email_thread("bjones@etlie.com", function.__name__, '<h2>' + str(value) + '</h2>')

        pass
    return wrapper


class Sendmail_Decorator(object):
    
    def __init__(self,function):

        print(type(function))

        self.message = str(object)
        # print(self.message)
        self._func = function

        
        # print(str(self._func))

        new_email_thread("bjones@etlie.com", "Processing Exception", str(self._func))
              
    def __call__(self,*args, **kwargs):

        print(f"calling _func {self._func}" )




    #     print(self._func)
    #     new_email_thread("bjones@etlie.com", "Processing Exception", "message")

    #     print("Email sent")
        
    #     return self._func()

