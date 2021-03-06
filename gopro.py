'''
    module containing the (virtual) gopro class and some usefull functions.
'''
 
import socket
from PIL import Image
import datetime
from threading import Thread
import csv
import time
from numpy import array as nparray
import os

curdir=os.path.dirname(__file__) 

 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8484 # Arbitrary non-privileged port
AREA = 4800 # pixel area of gopro lcd
WIDTH = 64  # pixels
HEIGHT = 75 # pixels

class gopro:
    """
    This class defines a gopro object. It will connect to a udp stream 
    from the gopro wifi remote. It keeps track of the states and triggers
    the write_start function when record is started and write_stop when 
    it is stopped. Run start() and stop() functions after initiation.
    Inputs:
        Optional:
            all default reply and stated values.
    """
    def __init__(self, filename='record_times.csv', image=os.path.join(curdir,'v-white.jpg'), 
                CM=[0,1], OO=[0], wt=[0], se=[0 for i in range(31)],
                cv=[1], pw=[0,1], st=[0,0,0,0,0], SH=[0,0]):
        self.values = {
            'cv':cv,
            'pw':pw,
            'st':st,
            'CM':CM,
            'OO':OO,
            'wt':wt,
            'se':se,
            'SH':SH
            }
        self.set_image(image);
        self.running = False
        self.filename = filename
        self.start_time = 0;
        self.stop_time = 0;
        
    def set_image(self,image):
        """
        Converts image to an array that will be printed on the lcd 
        screen when this gopro is the only one connected. (save into the lc 
        property of values)
        Arguments:
            image: path to a x image
        """
        self.values['lc'] = [0] + get_image_data(image)
        
    def start(self):
        """
        Starts thread that creates udp connection and opens a csv file 
        defined in initiation.
        """
        # create udp socket
        try :
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print 'Socket created'
        except socket.error, msg :
            print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            exit()
        # bind to host
        try:
            self.s.bind((HOST, PORT))
        except socket.error , msg:
            print 'Bind failed. Error Code : '+str(msg[0])+' Message '+msg[1]
            exit()
        # open file for writing and creat csv writter
        self.file = open(self.filename, 'wb')
        self.writer = csv.writer(self.file)
        # start thread
        self.running = True
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
    
    def run(self):
        """
        The function the thread runs in start.
        """
        while self.running:
            try:
                # receive data from client (data, addr)
                d = self.s.recvfrom(1024)
                data = d[0]
                addr = d[1]
                 
                if not data: 
                    print "No udp data => stopped"
                    break
                
                
                
                # make reply
                datarray = [ord(c) for c in data]
                #cmd = datarray[11:13]
                cmd = data[11:13]
                #print cmdstr
                
                # print recieved data
                # print get_hex_str(datarray)
                
                # change things before reply

                if cmd == 'CM':
                    # if mode is changed, change status
                    self.values['st'] = [0,datarray[13],0,0,0]


                if cmd == 'PW':
                    # change power state
                    #self.values['pw'] = [0,datarray[13]]
                    self.values['PW'] = datarray[13:]

                if cmd == 'SH':
                    # change shutter state
                    #self.values['pw'] = [0,datarray[13]]
                    #self.values['SH'] = datarray[13:]
                    self.values['st'][2] = datarray[13]
                    self.values['st'][4] = datarray[13]
                    if datarray[13] == 1:
                        self.start_time = datetime.datetime.now()
                        print "Start"
                    else:
                        self.stop_time = datetime.datetime.now()
                        self.writer.writerow([str(self.start_time),str(self.stop_time)])
                        print "Stop"
                
                datarray[13:] = self.values[cmd]

                reply = str(bytearray(datarray))
                
                # do things after reply is made

                if cmd == 'cv':
                    # after ok is sent send actual camera version next time
                    self.values['cv'] = [0,2,1,0x0c]
                    self.values['cv'] += [ ord(c) for c in 'HD3.03.03.00.Hero3-BlackEdition' ]


                self.s.sendto(reply , addr)

                # print sent data
                # print get_hex_str(datarray)
                
            except Exception as e:
                print e
                self.s.close()
                self.file.close()
                break
    
    def stop(self):
        """
        Stops thread and closes socket and file.
        """
        self.running = False
        time.sleep(0.5)
        self.s.close()
        self.file.close()
        return not self.thread.is_alive()

    
def get_image_data(image):
    """
    Puts converts image to an array, whose bit reprisentation reprisents
    the back and white values of the image. (binary data is captured in 
    reverse.
    Arguments:
        image: path to a x image
    """
    v = Image.open(image)
    vrgb = v.getdata()

    vb= ""
    for i in range(len(vrgb)):
        if vrgb[-i][0] < 100:
            vb += '1'
        else:
            vb += '0'

    a = [ int(vb[i:i+8],2) for i in range(0, len(vb), 8) ]
    return a
    
def get_int_array(hexstr):
    """
    returns an array of integers resulting from a string such as:
    00:00:01:3A
    """
    return [int(c,16) for c in hexstr.split(':')]
    
def get_hex_str(intarray):
    """
    Accepts array of integers and outputs a string of the form 00:01:3D
    """
    return ':'.join('%02x'%i for i in intarray)
    
    
def show_image(aa):
    """
    Displays the image defined by an integer array, as it will show on the 
    remote lcd.
    """
    astr = []
    for i in aa:
        b = bin(i)[2:]
        astr += [255]*(8-len(b))
        for c in b:
            if c=='0':
                astr += [255]
            else:
                astr += [0]


    aim = []
    for i in range(HEIGHT-1):
        col = astr[WIDTH*(HEIGHT-1-i):WIDTH*(HEIGHT-1-i+1)]
        aim.append(col)

    aim = np.array(aim)
    img = Image.fromarray(aim)
    img.show()
    

