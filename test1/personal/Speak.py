import os.path
from matplotlib.pyplot import Circle, subplots, gcf
from tkinter import Button, Tk, Frame, W, E, PhotoImage, Label, IntVar, Checkbutton, StringVar, OptionMenu
from itertools import islice
from pandas import read_excel



BASE = os.path.dirname(os.path.abspath(__file__))

def go(add_string):
    print(add_string)

def read_file():
    data = read_excel(os.path.join(BASE, "Rules_v10.xlsx"))
    print(data.iloc[0])
    lines = [line.rstrip('\n') for line in open(os.path.join(BASE, "text.txt"))]
    print(lines)
