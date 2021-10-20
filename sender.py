#!/usr/bin/env python

from __future__ import division
import cv2
import numpy as np
import socket
import struct
import math
import multiprocessing


class FrameSegment(object):
    """ 
    Object to break down image frame segment
    if the size of image exceed maximum datagram size 
    """
    # MAX_DGRAM = 2**16 ... for iOs operations should be less than 9216
    MAX_DGRAM = 2 ** 13
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64  # extract 64 bytes in case UDP frame overflown

    def __init__(self, sock, port, addr='127.0.0.1'):
        self.s = sock
        self.port = port
        self.addr = addr
        #print("sending config: IP = {}, PORT = {}. ".format(self.addr, self.port))

    def udp_frame(self, img):
        """ 
        Compress image and Break down
        into data segments 
        """
        compress_img = cv2.imencode('.jpg', img)[1]
        dat = compress_img.tostring()
        size = len(dat)
        count = math.ceil(size / self.MAX_IMAGE_DGRAM)
        array_pos_start = 0
        while count:
            array_pos_end = min(size, array_pos_start + self.MAX_IMAGE_DGRAM)
            self.s.sendto(struct.pack("B", count) +
                          dat[array_pos_start:array_pos_end],
                          (self.addr, self.port)
                          )
            tempString = "packet_i"
            self.s.sendto(tempString.encode(), ('127.0.0.1', 5005))
            array_pos_start = array_pos_end
            count -= 1


def send_status(port, status, ip='127.0.0.1'):
    #if __name__ == "__main__":
        BUFFER_SIZE = 1024

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host = socket.gethostname()  # Get the local machine name
        # print("i am : {}".format(host))
        s.connect((ip, port))
        s.send(status.encode())
        print("sended : {}".format(status))
        # data = s.recv(BUFFER_SIZE)
        s.close()
        #print("s closd _||")
        # print("received data: {}".format(data))


def stream(img):
    #if __name__ == "__main__":
        """ Top level main function """

        #print("sender working")

        # Set up UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = 5005

        fs = FrameSegment(s, port)

        fs.udp_frame(img)

        s.close()
