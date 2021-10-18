import redis
import config
import threading
import time


def callback(msg, **options):
    print('hi '+str(msg))
    key = msg['data'].decode('utf-8')
    print('key: '+key)
    print('something to cherry pick')


client = redis.StrictRedis()
pubsub = client.pubsub()
client.config_set('notify-keyspace-events','Ex')

# Set config in config file "notify-keyspace-events Ex"
# Subscribing to key expire events and whenver we get any notification sending it to event_handler function
pubsub.psubscribe(**{"__keyevent@0__:expired": callback})
pubsub.run_in_thread(sleep_time=0.01)

print('something else to cherry pick')

def alarm_missing_logic():
    """
    This logic will look at the heart beats in the timestamped records and compare it against the general inventory
    and it will create alerts when necessary.
    """
    client.set('expirekey', 2)
    client.expire('expirekey', 15)
    while True:
        time.sleep(5)
        client.persist('testkey')
        client.set('testkey', 2)
        client.expire('testkey', 15)



t1 = threading.Thread(target=alarm_missing_logic, args=[])
t1.start()




