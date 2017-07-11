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

treeView = fileList.FileList(".")
box = Gtk.Box(spacing = 10)
box.pack_start(treeView, True, True, 0)

sourceViewer = GtkSource.View()
box.pack_start(sourceViewer, True, True, 0)


win.add(box)

win.show_all()
Gtk.main()
