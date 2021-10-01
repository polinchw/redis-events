import redis
import config
import threading
import time

def callback(msg, **options):
    print('hi '+str(msg))
    key = msg['data'].decode('utf-8')
    print('key: '+key)


client = redis.Redis()
pubsub = client.pubsub()


# Set config in config file "notify-keyspace-events Ex"
# Subscribing to key expire events and whenver we get any notification sending it to event_handler function
pubsub.psubscribe(**{"__keyevent@0__:expired": callback})
pubsub.run_in_thread(sleep_time=0.01)


def alarm_missing_logic():
    """
    This logic will look at the heart beats in the timestamped records and compare it against the general inventory
    and it will create alerts when necessary.
    """
    while True:
        time.sleep(15)
        client.set('testkey', 2)
        client.expire('testkey', 5)


t1 = threading.Thread(target=alarm_missing_logic, args=[])
t1.start()




