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
treeView = fileList.FileList(".", sourceViewer)
box = Gtk.Box(spacing = 10)
box.pack_start(treeView, True, True, 0)

box.pack_start(sourceViewer, True, True, 0)

scrollWindow1 = Gtk.ScrolledWindow()
scrollWindow1.add(box)
win.add(scrollWindow1)

win.show_all()
Gtk.main()
