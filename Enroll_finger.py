#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from pyfingerprint.pyfingerprint import PyFingerprint


## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

def printID(number):
    print('Found template at position #' + str(positionNumber))
    f.loadTemplate(positionNumber, 0x01)
    characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
    print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to enroll new finger
try:
    print('Waiting for finger...')
    while ( f.readImage() == False ):    ## Wait that finger is read
        pass

    f.convertImage(0x01)## Converts read image to characteristics and stores it in charbuffer 1

    result = f.searchTemplate()## Checks if finger is already enrolled
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        printID(positionNumber)

    print('Remove finger...')
    time.sleep(2)
    print('Waiting for same finger again...')

    while ( f.readImage() == False ):## Wait that finger is read again
        pass
    f.convertImage(0x02)## Converts read image to characteristics and stores it in charbuffer 2


    if ( f.compareCharacteristics() == 0 ):## Compares the charbuffers
        raise Exception('Fingers do not match')
    f.createTemplate()## Creates a template

    ## Saves template at new position number
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    printID(positionNumber)

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
