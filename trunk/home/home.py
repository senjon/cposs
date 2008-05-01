#!/usr/bin/env python

try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	print "PyGTK Not found"
try:
	import sys
	import gtk
	import gtk.glade
	import gobject
	import logging
	import shelve
	import os
	import locale
	import gettext
except:
	print "Import error, home cannot start. Check your dependencies."
	sys.exit(1)

FILE_EXT = "home"
APP_NAME = "home"

class home:
	"""The home class"""

	def __init__(self, parent, tab):
		
		self.parent=parent

		# Set the project file
		self.project_file = ""

		#Set the Glade file
		self.gladefile = "Glade/home.glade"

		self.wTree = gtk.glade.XML(self.gladefile,"vbox1");
		_label = gtk.Label();
        	_label.set_text("Home Screen")
        	
		tab.append_page(self.wTree.get_widget("vbox1"),_label);

		parent.printme()

		#Initiate the textview element on the GUI
		self.logwindowview=self.wTree.get_widget("Description")
		self.bufferDescription=gtk.TextBuffer(None)
		self.logwindowview.set_buffer(self.bufferDescription)
	
		#Create the dictionary of events and create them
		dic = {		"on_Home_destroy" : self.on_Quit
				, "on_txtBarcode_changed" : self.OnBarcodeChange
				, "on_btnBasket_clicked" : self.OnBasketClick}
		self.wTree.signal_autoconnect(dic)

		#Print out the command line arguments
		#print sys.argv

		#Setup logging
		logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',filename='debug.log')

	def on_Quit(self, widget):
		"""Called when the application is going to quit"""
		gtk.main_quit()

	def OnBarcodeChange(self, widget):
		"""Called when the user types in the text area."""
		ItemID=int(self.wTree.get_widget("txtBarcode").get_text() or 0)
		logging.debug('Barcode changed to %s', ItemID)
		self.parent.printme()
        	ItemDetails=self.parent.database.ProductDictionary(ItemID) 
        	for ControlName in [ "Heading", "Detail1", "Detail2", "Price" ]:
			self.wTree.get_widget(ControlName).set_text("%s" % ItemDetails[ControlName])
		#Simply adds text to the buffer which is being shown in the textarea		
		self.bufferDescription.insert_at_cursor("%s" % ItemDetails["Description"],len("%s" % ItemDetails["Description"]))		
		#print ItemDetails

	def OnBasketClick(self, widget):
		"""Called when we want to take the product to the sale screen"""
		basketScreen=basket.Basket()

	def printme(self):
		print "Shit it printed"
	
	def show_error_dlg(self, error_string):
		"""This Function is used to show an error dialog when
		an error occurs.
		error_string - The error string that will be displayed
		on the dialog.
		"""
		error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR
					, message_format=error_string
					, buttons=gtk.BUTTONS_OK)
		error_dlg.run()
		error_dlg.destroy()

if __name__ == "__main__":
	home = home()
	gtk.main()
	
