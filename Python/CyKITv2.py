


import sys
import select
import struct
import eeg
import time


def main():
    global cyHeadset
    myi = eeg.MyIO()
    parameters = "info+confirm"
    cyHeadset = eeg.EEG(6, myi, parameters)
    

def get_data():
    return cyHeadset.get_data()

main()
get_data()