import numpy as np
import sys
from tkinter import Tk, Toplevel, Event, TclError, StringVar, Frame, Menu, \
    Label, Entry, SOLID, RIDGE, LEFT, messagebox, IntVar, Scrollbar, RIGHT, BOTTOM, TOP, RIDGE,\
    Listbox, END
from tkinter.ttk import Combobox, Notebook, Checkbutton
import tkinter as tk
import pandas as pd
import tksheet
import time
from operator import mul, sub, add
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfile
from datetime import date
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

import os.path
from os import path

sys.path.append("..")
from nse_data_fetcher import nse_connector as NC


font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 4}

from matplotlib import rc
rc('font', **font)
