import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from chord import *
node3= ChordNode(Address("127.0.0.1",("5132","5008","5048")), local= True)