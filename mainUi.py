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

win = Gtk.Window(title="mainWindow")
win.connect("delete-event", Gtk.main_quit)

fileList = Gtk.TreeStore(str)
firstFile = fileList.append(None,["abc"])
fileList.append(firstFile,["sun"])

fileList.append(None,["def"])

treeView = Gtk.TreeView(fileList)
renderer = Gtk.CellRendererText()
column = Gtk.TreeViewColumn("File", renderer, text=0)
treeView.append_column(column)

win.add(treeView)

treeView.show()
win.show_all()
Gtk.main()
