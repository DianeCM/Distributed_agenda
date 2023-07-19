import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from chord import *
node1= ChordNode(Address("127.0.0.1",("5030","5002","5042","5792")), local= True)