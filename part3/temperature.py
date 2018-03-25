import random
import tkinter as tk
from tkinter import Tk, Entry, Button, INSERT, Text
from tkinter.ttk import *
import subprocess
import time
import io
import os
import dis

class Temperature(object):
	def __init__(self):
		self.temperature = 0
		self.obeservers = []

	def setTemperature(self, newTemperature):
		self.temperature = newTemperature
		for callback in self.obeservers:
			callback(self.temperature)

	def bind(self, callback):
		self.obeservers.append(callback)

class CriticalFrame(tk.Frame):
	def __init__(self, temperature, master=None):
		super().__init__(master)
		tempearture.bind(self.criticalTemp())

	def criticalTemp(self):
		temperature = Temperature()

		e = Entry(self)
		e.pack(side='top', anchor='n')
		b = Button(root, text='Set Critical Temperature', command=app)
		b.pack(side='top', fill="y", expand=True)

	def set_callback(self, a_func):
		self.callback = a_func

class TemperatureFrame(tk.Frame):
	def __init__(self, tempearture, master=None):
		super().__init__(master)
		self.createText()
		tempearture.bind(self.updateTemperature)
		self.degree_sign= u'\N{DEGREE SIGN}'

	def createText(self):
		self.temperatureLabel = tk.Label(self.master, font=('Arial', 100))
		self.temperatureLabel.pack(side = tk.RIGHT)

	def updateTemperature(self, temperature):
		self.celsius = (temperature - 32) * (5/9)
		self.celsius = float("{0:.2f}".format(self.celsius))
		self.text = str(temperature) + self.degree_sign + 'F\n' + str(self.celsius) + self.degree_sign + 'C'
		self.temperatureLabel['text'] = format(self.text)
		if (temperature >= 80):
			self.temperatureLabel['fg'] = 'red'
		elif (temperature >= 60):
			self.temperatureLabel['fg'] = 'green'
		else:
			self.temperatureLabel['fg'] = 'blue'
			
class ThermometerFrame(tk.Frame):
	def __init__(self, temperature, master=None):
		super().__init__(master)
		self.canvas = tk.Canvas(self, width = 1200, height = 800)
		self.canvas.pack(side = tk.LEFT)

		self.photo = tk.PhotoImage(file = '/home/ryan/thermometer.gif')
		self.canvas.create_image(200, 300, image = self.photo)
		self.canvas.create_oval(200 - 42, 530 - 42, 200 + 42, 530 + 42, fill = 'red')
		temperature.bind(self.drawMercury)

	def drawMercury(self, temperature):
		self.canvas.delete('line')
		self.critTemp = 80
		self.drawHeight = 530 - temperature * 4
		if (self.drawHeight <= 80):
			self.drawHeight = 80
		self.canvas.create_line(200, 530, 200, self.drawHeight, width = 35, fill = 'red', tag = 'line')

class Application(tk.Frame):
	def __init__(self, temperature, master = None):
		super().__init__(master)
		self.pack()
		self.initFrames(temperature)

	def initFrames(self, temperature):
		self.temperatureFrame = TemperatureFrame(temperature, self)
		self.temperatureFrame.pack(side = tk.RIGHT)
		self.thermometerFrame = ThermometerFrame(temperature, self)
		self.thermometerFrame.pack(side = tk.LEFT)

if __name__ == '__main__':
	window = tk.Tk()
	window.wm_title('Temperature')
	window.geometry('1200x600')
	temperature = Temperature()
	app = Application(temperature, master = window)

	while True:
		newTemperature = random.uniform(30, 106)
		temperature.setTemperature(int(newTemperature))     
		window.update_idletasks()
		window.update()

		time.sleep(5) #5 second delay
