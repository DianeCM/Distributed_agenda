import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from chord import *
node= ChordNode(Address("127.0.0.1",("5050","5001","5044","5790")), local= True)