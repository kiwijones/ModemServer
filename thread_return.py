
from queue import Queue # Python 3.x
from threading import Thread

def foo(bar):
  
    print('hello {0}'.format(bar))   # Python 3.x
    return 'hello {0}'.format(bar)


que = Queue()           # Python 3.x

threads_list = list()

for r in range(0,10):

    t = Thread(target=lambda q, arg1: q.put(foo(r)), args=(que, 'world!'))
    t.start()

# t2 = Thread(target=lambda q, arg1: q.put(foo(arg1)), args=(que, 'world!'))
# t2.start()

threads_list.append(t)

# Add more threads here
# ...
# threads_list.append(t2)
# ...
# threads_list.append(t3)
# ...

# Join all the threads
for t in threads_list:
    t.join()

# Check thread's return value
while not que.empty():
    result = que.get()
    
    print(f"result {result}")       # Python 3.x