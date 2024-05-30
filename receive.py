import pika, sys, os

def main():



    userName = "test1"
    password = "H64M2wksSsPLcuy"
    host = "92.51.204.82"

    credentials = pika.PlainCredentials(username=userName, password=password)

    parameters = pika.ConnectionParameters(host,
                                        5672,
                                        '/',
                                        credentials)



    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='stormReceive')

    def callback(ch, method, properties, body):
        
        print(" [x] Received %r" % body.decode())
        

    channel.basic_consume(queue='stormReceive', on_message_callback=callback, auto_ack=True)

    # print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)