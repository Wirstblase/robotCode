#///IMPORTS START
#imported in v1
import cv2
import time
import serial
import os
import sys
import select
import numpy as np
import thread
from picamera.array import PiRGBArray
from picamera import PiCamera
import socket
#imported in v2
from micropyGPS import MicropyGPS
from os import system, name
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
#///IMPORTS END

sMode = 0# 0-use to show debug data in console , 1-use to enable video streamer
'''For video streamer run with:
sudo python robot_code_1_0.py | cvlc --demux=rawvideo --rawvid-fps=30 --rawvid-width=320 --rawvid-height=180 --rawvid-chroma=RV24 -vvv stream:///dev/stdin --sout '#transcode{vcodec=mp4v}:rtp{sdp=rtsp://:8154/}'
'''
connectionType = 0# 0-use WI-FI, 1-use SERVER, 2-use bluetooth?

debugMode = True #leave it true while still in dev stage, False for deployment

bodyType = 0 

loggedIn = 0

'''
-1 -Custom settings adaptable by the user (W.I.P)
0 -Settings adapted for the first body type, aka the OG
1 -Settings adapted for the second body type, aka the BIG BOI
'''

CPUTemp = 0 #variable for showing the temperature of the CPU
overheat = 0 #1-mild overheat 2-significant overheat 3-extreme overheat

my_gps = MicropyGPS()
my_sentence = ''

AICarDetection = 0 # 0 - AICarDetection - off , 1-Will draw a green rectangle over any car it sees
AIItemDetection = 0 # 0- AIItemDetection - off , 1-Will draw a green rectangle over any desired object it sees

class SocketServer:
	def __init__(self, host = '0.0.0.0', port = 6969):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.host = host
		self.port = port
		self.sock.bind((host,port))
		self.sock.listen(1)
	def close(self):
		global sMode
		if(sMode == 0):
			print('Closing server socket (host {}, port {})'.format(self.host,self.port))
		if (self.sock):
			self.sock.close()
			self.sock = None
	def run_server(self):
		global sMode
		if(sMode == 0):
			print('Starting socket server (host {},port {})'.format(self.host,self.port))
		client_sock, client_addr = self.sock.accept()
		if(sMode == 0):
			print('Client {} connected'.format(client_addr))
		stop = False
		while not stop:
			if client_sock:
				try:
					rdy_read, rdy_write, sock_err = select.select([client_sock,],[],[])
				except select.error:
					if(sMode == 0):
						print('select() failed on socket with {}'.format(client_addr))
					s.write('x')
					return 1
				
				if len(rdy_read) > 0:
					read_data = client_sock.recv(255)
					if len(read_data) == 0:
						if(sMode == 0):
							print('{} closed the socket'.format(client_addr))
						s.write('x')
						stop = True
					else:
						if(sMode == 0):
							print('>>> Received: {}'.format(read_data.rstrip()))
						if(read_data.rstrip() == 'Quit'):
							stop = True
						else:
							client_sock.send(read_data)
						global AICarDetection
						if(read_data.rstrip() == 'w'):
							goFwd()
						elif(read_data.rstrip() == 'a'):
							steerLeft()
							s.write('a')
						elif(read_data.rstrip() == 'd'):
							steerRight()
							s.write('d')
						elif(read_data.rstrip() == 's'):
							goBwd()
						elif(read_data.rstrip() == 'h'):
							client_sock.send("                 "+s.readline())
						elif(read_data.rstrip() == 'ir'):
							s.write("t")
						elif(read_data.rstrip() == 'ri'):
							s.write("T")
						elif(read_data.rstrip() == 'aux'):
							s.write("g")
						elif(read_data.rstrip() == 'xua'):
							s.write("G")
						elif(read_data.rstrip() == 'mod'):
							s.write("b")
						elif(read_data.rstrip() == 'dom'):
							s.write("B")
						elif(read_data.rstrip() == '0'):
							s.write("0")
						elif(read_data.rstrip() == '1'):
							s.write("1")
						elif(read_data.rstrip() == '2'):
							s.write("2")
						elif(read_data.rstrip() == '3'):
							s.write("3")
						elif(read_data.rstrip() == '4'):
							s.write("4")
						elif(read_data.rstrip() == '5'):
							s.write("5")
						elif(read_data.rstrip() == '6'):
							s.write("6")
						elif(read_data.rstrip() == '7'):
							s.write("7")
						elif(read_data.rstrip() == '8'):
							s.write("8")
						elif(read_data.rstrip() == '9'):
							s.write("9")
						elif(read_data.rstrip() == '*'):
							s.write("*")
						elif(read_data.rstrip() == '@'):
							s.write("@")
						elif(read_data.rstrip() == 'z'):
							s.write("z")
						elif(read_data.rstrip() == 'car'):
							AICarDetection = 1
						elif(read_data.rstrip() == 'rac'):
							AICarDetection = 0
						#client_sock.send("  ArduinoSensor: "+s.readline())
							
						
							
			else:
				if(sMode == 0):
					print("No client is connected")
				stop = True
		if(sMode == 0):	
			print('Closing connection with {}'.format(client_addr))
		client_sock.close()
		return 0
		

s = serial.Serial('/dev/ttyUSB0', 19200) #the Serial module that communicates with the motherboard
internalserial = serial.Serial(
	port = '/dev/ttyS0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout = 1
) #The on-board serial of the raspberry pi (now used for GPS)


displayMode = 0 # 0-Startup screen 1-ID 2-IDLE 3-DebugInfo

#///START DISPLAY INIT
#Pin configuration to use the OLED
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()
#///END DISPLAY INIT

camera = PiCamera()
camera.resolution=(320,180)
camera.framerate=20

time.sleep(0.1)
rawCapture=PiRGBArray(camera, size=(320,180)) # OPENCV

#Object recognition config & training
MIN_MATCH_COUNT=30
surf = cv2.xfeatures2d.SIFT_create()
detector = surf
FLANN_INDEX_KDTREE=0
flannParam=dict(algorithm=FLANN_INDEX_KDTREE, tree=5)
flann=cv2.FlannBasedMatcher(flannParam,{})

trainImg=cv2.imread('raspiboxlowres.jpg',0) #!!!The image used to train the AI to recognize an image
trainKP,trainDecs=detector.detectAndCompute(trainImg,None)
#Object recognition config & training

car_cascade = cv2.CascadeClassifier('cars.xml') #The trained data for car recognition

goingLeft = False
goingRight = False
goingFwd = False
goingBwd = False

connectedToApp = False

connectedToMotherboard = False

sensorData = "none"
shouldRefreshData = False	
	

def clear():
	_=system('clear')
	
def brake():
	global goingBwd
	global goingFwd
	if(goingFwd == True):
		s.write('x')
		if(sMode == 0):	
			print("Braking...")
		goingFwd = False
	if(goingBwd == True):
		s.write('x')
		goingBwd = False
		if(sMode == 0):	
			print("Braking...")


def goFwd():
	global goingFwd
	if(goingBwd == True):
		brake()
	else:
		if(goingBwd == False):
			s.write('w')
			if(sMode == 0):	
				print("Should be going forward")
			goingFwd = True
	
def goBwd():
	global goingBwd
	if(goingFwd == True):
		brake()
	else:
		if(goingFwd == False):
			s.write('s')
			goingBwd = True
			if(sMode == 0):	
				print("Should be going back")
	
def steerLeft():
	global goingLeft
	global goingRight
	if(goingRight == True):
		goingRight = False
		s.write('a')
		if(sMode == 0):	
			print("Should be going left")
		goingLeft = True

	
	
def steerRight():
	global goingLeft
	global goingRight
	if(goingLeft == True):
		goingLeft = False
		s.write('d')
		if(sMode == 0):	
			print("Should be going right")
		goingRight = True

def steerCenter():
	global goingLeft
	global goingRight
	goingLeft = False
	goingRight = False
	s.write('z')
	
def checkConnections():
	global connectedToApp
	global displayMode
	global loggedIn
	if(debugMode == False):
		time.sleep(30)
		if(connectedToApp == False):
			os.system("sudo systemctl stop hostapd")
		
	else:
		if(debugMode == True):
			if(sMode == 0):	
				print("'checkConnections' Started")
				time.sleep(30)
				print("30 SECONDS PASSED")
				if(loggedIn == 0):
					displayMode = 1
			
def measure_temp():
	global CPUTemp
	temp = os.popen("vcgencmd measure_temp").readline()
	return (temp.replace("temp= ", ""))

def setup():
	global connectedToMotherboard
	global debugMode
	global sMode

	if(debugMode):
		if(sMode == 0):	
			print("Starts setting up")
	
	if(bodyType==0):	
		s.write('0')
		time.sleep(1)
		s.write('2')
		s.write('3')
		s.write('2')
		s.write('0')
		s.write('x') #initializes ESC making sure it is stopped
		
	thread.start_new_thread(loop2, ()) #Camera & AI
	thread.start_new_thread(loop3, ()) #Server
	thread.start_new_thread(checkConnections, ()) #Determines if it should use wifi or gsm
	thread.start_new_thread(loop4, ()) #Refreshes the GPS Data and updates its corresponding variables
	thread.start_new_thread(loop5, ()) #Refreshes the OLED display data and updates it
	
	'''
	ser.write('C\n')
	while(not connectedToMotherboard):
		if(debugMode == True):
			print("Waiting for motherboard to respond with Y")
		x=s.readline()
		if(x=="Y"):
			connectedToMotherboard = True'''
	
loop2running = False
loop3running = False	
	
def loop2():
	global loop2running
	global sMode
	global AICarDetection
	global AIItemDetection
	loop2running = True
	for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):  #default = bgr
		image=frame.array
		
		if(AICarDetection == 1):
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			#detect cars in the video
			cars = car_cascade.detectMultiScale(gray, 1.1, 3)
			#to draw arectangle in each cars 
			for (x,y,w,h) in cars:
				cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
				
		#if(AIItemDetection == 1):
		
			  
		cv2.imshow("Frame",image)
			
		if(sMode==1):
				sys.stdout.write(image.tostring())
		
		
		key=cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
		
		
		
def main():
	global connectionType
	server = SocketServer()
	if(connectionType == 0):
		server.run_server()
	
def loop3(): #Loops the server commands
	while True:
		global loop3running
		loop3running = True
		if __name__ == "__main__":
			main()

runonce = 0 #tells the first loop function what stuff to do only once

def loop():
	global loop2running
	global runonce
	global sMode
	if(runonce == 0):
		if(debugMode):
			runonce = 1
			if(sMode == 0):	
				print("Loop 1 running!")
			if(loop2running == True):
				if(sMode == 0):	
					print("Loop 2 running!")
			
def loop4():
	global sMode
	global debugMode
	global CPUTemp
	
	while True:
		if(debugMode==1):
			time.sleep(0.1)
			clear()
		my_sentence = internalserial.readline()
		for x in my_sentence:
			my_gps.update(x)
		if(sMode==0):
			print('Lat:')
			print(my_gps.latitude_string())
			print('Lon:')
			print(my_gps.longitude_string())
			print('Alt:')
			print(my_gps.altitude)
			print('Spd:')
			print(my_gps.speed_string('kph'))
			print('Satellites connected:')
			print(my_gps.satellites_in_use)
			print('Course')
			print(my_gps.course)
			
			
startupimageshown = 0 #Tells the display function to display the startup screen
def loop5():
	while True:
		global displayMode
		global startupimageshown
	
		if(displayMode == 1):
			image = Image.open('ID.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
			disp.image(image)
			disp.display()
		
		if(displayMode == 0):
			if(startupimageshown == 0):
				image = Image.open('HI.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
				disp.image(image)
				disp.display()
				startupimageshown = 1
				time.sleep(5)
				disp.clear()
				disp.display()
				displayMode = 2
			
		if(displayMode == 2):
			image = Image.open('IDLE.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
			disp.image(image)
			disp.display()
			
		if(displayMode == 3):
			disp.clear()
			disp.display()
	
			
		
setup()

while True:
	loop()
	time.sleep(1)
