from channel import *
from utils import *
import threading
import time

channel = Channel(Address("*","5555")) 
channel.run()
#key = random.randint(0,pow(2,159))

#my_thread= threading.Thread(target=channel.run())
#my_thread = threading.Thread(target=channel.lookup_key(key))