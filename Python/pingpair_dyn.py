#!/usr/bin/env python

#
# Example using Dynamic Payloads
# 
#  This is an example of how to use payloads of a varying (dynamic) size.
# 

import time, os, sys
from RF24 import *

#print sys.path
#print "RF24-library path:", os.path.dirname(RF24.__file__)

# CE Pin, CSN Pin, SPI Speed

# Setup for GPIO 22 CE and GPIO 25 CSN with SPI Speed @ 1Mhz
#radio = radio(RPI_V2_GPIO_P1_22, RPI_V2_GPIO_P1_18, BCM2835_SPI_SPEED_1MHZ)

# Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 4Mhz
#radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_4MHZ)

# Setup for GPIO 22 CE and CE1 CSN with SPI Speed @ 8Mhz
radio = RF24(RPI_V2_GPIO_P1_22, RPI_V2_GPIO_P1_24, BCM2835_SPI_SPEED_8MHZ)

# Setup for GPIO 22 CE and CE0 CSN for RPi B+ with SPI Speed @ 8Mhz
#radio = RF24(RPI_BPLUS_GPIO_J8_22, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)


pipes = [0xA0, 0xF0]
#pipes = [0xA0, 0xF0]
#min_payload_size = 4
#max_payload_size = 32
#payload_size_increments_by = 1
#next_payload_size = min_payload_size
inp_role = 'none'
send_payload = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ789012'
millis = lambda: int(round(time.time() * 1000))

print 'pyRF24/examples/pingpair_dyn/'
radio.begin()
#radio.enableDynamicPayloads()
radio.setAddressWidth(5)
radio.setChannel(0x4c)
radio.setAutoAck(0)
radio.setRetries(15,15)
radio.setDataRate(RF24_1MBPS)
radio.payloadSize = 32
radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1,pipes[0])
radio.startListening()
radio.printDetails()

"""
print ' ************ Role Setup *********** '
while (inp_role !='0') and (inp_role !='1'):
    inp_role = raw_input('Choose a role: Enter 0 for receiver, 1 for transmitter (CTRL+C to exit) ')

if inp_role == '0':
    print 'Role: Pong Back, awaiting transmission'
    radio.openWritingPipe(pipes[1])
    radio.openReadingPipe(1,pipes[0])
    radio.startListening()
else:
    print 'Role: Ping Out, starting transmission'
    radio.openWritingPipe(pipes[0])
    radio.openReadingPipe(1,pipes[1])
"""

# forever loop
while 1:
    """
    if inp_role == '1':   # ping out
        # The payload will always be the same, what will change is how much of it we send.

        # First, stop listening so we can talk.
        radio.stopListening()

        # Take the time, and send it.  This will block until complete
        print 'Now sending length ', next_payload_size, ' ... ',
        radio.write(send_payload[:next_payload_size])

        # Now, continue listening
        radio.startListening()

        # Wait here until we get a response, or timeout
        started_waiting_at = millis()
        timeout = False
        while (not radio.available()) and (not timeout):
            if (millis() - started_waiting_at) > 500:
                timeout = True

        # Describe the results
        if timeout:
            print 'failed, response timed out.'
        else:
            # Grab the response, compare, and send to debugging spew
            len = radio.getDynamicPayloadSize()
            receive_payload = radio.read(len)

            # Spew it
            print 'got response size=', len, ' value="', receive_payload, '"'

        # Update size for next time.
        next_payload_size += payload_size_increments_by
        if next_payload_size > max_payload_size:
            next_payload_size = min_payload_size
        time.sleep(0.1)
    """
    #else:
        # Pong back role.  Receive each packet, dump it out, and send it back
    # if there is data ready
    #print "Waiting for data"
    if radio.available():
        print "Radio avail"
        while radio.available():
        # Fetch the payload, and see if this was the last one.
	    len = radio.getDynamicPayloadSize()
	    receive_payload = radio.read(len)

	    # Spew it
	    print 'Got payload size=', len, ' value="', receive_payload, '"'

        # First, stop listening so we can talk
        radio.stopListening()

        # Send the final one back.
        try:
            radio.write(receive_payload)
            print 'Sent response.'
        except NameError:
            print 'Error in reading payload, trying again..'
            pass
        # Now, resume listening so we catch the next packets.
        radio.startListening()
