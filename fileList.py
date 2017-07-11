import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os
import rlcompleter
import pdb

pdb.Pdb.complete= rlcompleter.Completer(locals()).complete


class FileList(Gtk.TreeView):

    def buttonCallback(self, path, view_column , userPar):
        pdb.Pdb.complete= rlcompleter.Completer(locals()).complete
        pdb.set_trace()
        print path
        print view_column

    def __init__(self, mainDirectory):
        Gtk.TreeView.__init__(self)

        fileList = Gtk.TreeStore(str)

        dirHash = {}

        for root, dirs, files in os.walk(mainDirectory, topdown = True):
            
            print "iteration"
            for name in files:
                if root in dirHash:
                    parent = dirHash[root]
                else:
                    parent = None
                lbl = name
                fileList.append(parent,[lbl])
                print (os.path.join(root, name))

            for name in dirs:
                
                if root in dirHash:
                    parent = dirHash[root]
                else:
                    parent = None

                lbl = name
                thisDir = fileList.append(parent,[lbl])
                indexStr = os.path.join(root, name)
                dirHash[indexStr] = thisDir
                print (os.path.join(root, name))

        self.connect('row-activated', self.buttonCallback)

        self.set_model(fileList)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("File", renderer, text=0)
        self.append_column(column)


