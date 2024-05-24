import pika, sys, os

def main():



    userName = "vend"
    password = "YHgc7RLiNJaJVmx"
    host = "vpn.etlie.com"

    credentials = pika.PlainCredentials('modems', 'v5aWf74MrcDh4Tb')

    parameters = pika.ConnectionParameters(host,
                                        5672,
                                        '/',
                                        credentials)



    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='Storm-Modems')

    def callback(ch, method, properties, body):
        
        print(" [x] Received %r" % body.decode())

    channel.basic_consume(queue='Storm-Modems', on_message_callback=callback, auto_ack=True)

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