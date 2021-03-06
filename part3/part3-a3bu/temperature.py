import random
import tkinter as tk
import subprocess
#import pygame
import time
import serial
import io
import os
import RPi.GPIO as GPIO

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

class TemperatureFrame(tk.Frame):
    def __init__(self, tempearture, master=None):
        super().__init__(master)
        self.createText()
        tempearture.bind(self.updateTemperature)

    def createText(self):
        self.temperatureLabel = tk.Label(self.master, text=u'0\u2109', font=('Arial', 200))
        self.temperatureLabel.pack(side = tk.RIGHT)

    def updateTemperature(self, temperature):
        self.temperatureLabel['text'] = u'{}\u2109'.format(temperature)
        if (temperature >= 80):
            self.temperatureLabel['fg'] = 'red'
        else:
            self.temperatureLabel['fg'] = 'black'

    #def playSound(self, temperature):
        #if (temperature >= 80):
            #pygame.mixer.music.player()
            #while pygame.mixer.music.get_busy() == True:
                #continue

class ThermometerFrame(tk.Frame):
    def __init__(self, temperature, master=None):
        super().__init__(master)
        self.canvas = tk.Canvas(self, width = 800, height = 800)
        self.canvas.pack(side = tk.LEFT)

        self.photo = tk.PhotoImage(file = '/home/pi/Desktop/thermometer.gif')
        self.canvas.create_image(200, 300, image = self.photo)
        self.canvas.create_oval(200 - 42, 530 - 42, 200 + 42, 530 + 42, fill = 'red')
        temperature.bind(self.drawMercury)

    def drawMercury(self, temperature):
        self.canvas.delete('line')
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
    root = tk.Tk()
    root.wm_title('Temperature')
    root.geometry('800x600')
    temperature = Temperature()
    app = Application(temperature, master = root)
    ser=serial.Serial('/dev/ttyAMA0')

    while True:
##        newTemperature = random.randint(60, 106)
##        temperature.setTemperature(newTemperature)
        
        x=ser.read(4)
        bytes=x.rstrip(b'\x00')
        newTemperature=int(bytes.decode('utf-8'))
##        root.update_idletasks()
##        root.update()
        temperature.setTemperature(newTemperature)
            
        root.update_idletasks()
        root.update()
        
        if (newTemperature >= 80):
            os.system('aplay ./boing_x.wav')
        #print(type(y))
        #temperature.setTemperature(65)

        #time.sleep(5) #5 second delay
