import readline
def completer(text, state):
        options = [i for i in commands if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

import gi
gi.require_version('Gtk', '3.0')
import fileList
from gi.repository import Gtk
from gi.repository import GtkSource 
import numpy as np

win = Gtk.Window(title="mainWindow")
win.connect("delete-event", Gtk.main_quit)


win.set_default_size(400, 300)
f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
t = np.arange(0.0, 3.0, 0.01)
s = np.sin(2*np.pi*t)
a.plot(t, s)

canvas = FigureCanvas(f)  # a gtk.DrawingArea
sw = Gtk.ScrolledWindow()
sw.add_with_viewport(canvas)
win.add(sw)

treeView = fileList.FileList(".", a)
box = Gtk.Box(spacing = 10)
box.pack_start(treeView, True, True, 0)


scrollWindow1 = Gtk.ScrolledWindow()
scrollWindow1.add(box)
win.add(scrollWindow1)

win.show_all()
Gtk.main()
