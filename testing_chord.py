from channel import *
from utils import *
import threading
import time

channel = Channel(Address("127.0.0.1","5555")) 
channel.run()