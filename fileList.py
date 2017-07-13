import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os
import rlcompleter
import pdb

from gi.repository import GtkSource 
from gi.repository import Gio 

pdb.Pdb.complete= rlcompleter.Completer(locals()).complete


class FileList(Gtk.TreeView):

    def buttonCallback(self, path, view_column , userPar):
        #pdb.Pdb.complete= rlcompleter.Completer(locals()).complete
        #pdb.set_trace()

        fileName = self.fileTable[view_column.to_string()]
        bufferText = self.sourceViewer.get_buffer()
        bufferText.set_text(open(fileName).readlines())

        print fileName

    def __init__(self, mainDirectory, sourceViewer):
        Gtk.TreeView.__init__(self)

        fileList = Gtk.TreeStore(str)
        self.sourceViewer = sourceViewer

        dirHash = {}
        self.fileTable = {}
        for root, dirs, files in os.walk(mainDirectory, topdown = True):
            
            print "iteration"
            for name in files:
                if root in dirHash:
                    parent = dirHash[root]
                else:
                    parent = None
                lbl = name
                fileIter = fileList.append(parent,[lbl])
                pathStr = fileList.get_string_from_iter(fileIter)
                self.fileTable[pathStr] = os.path.join(root, name)
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


