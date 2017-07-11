import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os

class FileList(Gtk.TreeStore):
    def __init__(self):
        super(str).__init__(str)

        firstFile = self.append(None,["abc"])
        fileList.append(firstFile,["sun"])

        fileList.append(None,["def"])

