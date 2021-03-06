# Kenneth Latiemr
# 9/9/2017
# Description:
# 	main file for controlling the tachometer and character LCD.

import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import obd
import time
import threading

from led_tachometer import tachometer

global connection
global rpm

class led_thread(threading.Thread):
	def __init__(self):
		self.tach = tachometer()
		threading.Thread.__init__(self)
		self._running = True
	def run(self):
		global rpm
		while True:
			try:
				self.tach.display_rpm(int(rpm))
				time.sleep(0.05)
			except RuntimeError:
				pass

class lcd_thread(threading.Thread):
	def __init__(self):
		lcd_rs = 27
		lcd_en = 22
		lcd_d4 = 16
		lcd_d5 = 12
		lcd_d6 = 25
		lcd_d7 = 7
		lcd_backlight = 21
		lcd_columns = 16
		lcd_rows = 2
		self.lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
			   							lcd_columns, lcd_rows, lcd_backlight)
		self.lcd.set_backlight(1)
		threading.Thread.__init__(self)
		self._running = True
	def run(self):
		global rpm
		while True:
			try:
				self.lcd.message('%s %s' % ('RPM:\n', rpm))
				time.sleep(0.25)
			except RuntimeError:
				pass

if __name__ == "__main__":
	rpm = 0
	connection = obd.Async() # asynchronous connection
	def new_rpm(response):
		global rpm
		rpm = response.value.magnitude
	connection.watch(obd.commands.RPM, callback=new_rpm)
	connection.start()
	while connection.status == obd.OBDStatus.NOT_CONNECTED:
		time.sleep(0.1)
	thread_2 = lcd_thread()
	thread_2.start()
	thread_1 = led_thread()
	thread_1.start()
	
