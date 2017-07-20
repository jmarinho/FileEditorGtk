import readline
def completer(text, state):
        options = [i for i in commands if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import fileList
from gi.repository import GtkSource 

win = Gtk.Window(title="mainWindow")
win.connect("delete-event", Gtk.main_quit)

sourceViewer = GtkSource.View()
sourceViewer.set_show_line_numbers(True)

tabs = Gtk.Notebook()

treeView = fileList.FileList(".", sourceViewer, tabs)
box = Gtk.Box(spacing = 10)


scrollWindow1 = Gtk.ScrolledWindow()
scrollWindow1.add(treeView)
scrollWindow1.set_size_request(200,500)

box.pack_start(scrollWindow1, True, True, 0)
box.pack_start(tabs, True, True, 0)
win.add(box)

win.resize(500,1000)
win.show_all()
Gtk.main()
