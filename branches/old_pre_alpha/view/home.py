#!/usr/bin/env python

try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	print _("PyGTK Not found")
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
	print _("Import error, home cannot start. Check your dependencies.")
	sys.exit(1)

FILE_EXT = "home"
APP_NAME = "home"

class home:
	"""The home class"""

	def __init__(self, parent, tab):
		
		self.parent=parent

		#self.parent.printme()
		# Set the project file
		self.project_file = ""

		#Set the Glade file
		self.gladefile = "glade/home.glade"

		self.wTree = gtk.glade.XML(self.gladefile,"vbox1");
		_label = gtk.Label();
        	_label.set_text(_("Home Screen"))
        	
		tab.append_page(self.wTree.get_widget("vbox1"),_label);

		#Initiate the textview element on the GUI
		self.logwindowview=self.wTree.get_widget("Description")
		self.bufferDescription=gtk.TextBuffer(None)
		self.logwindowview.set_buffer(self.bufferDescription)
	
		self.labelNames=[ "Heading", "Detail1", "Detail2", "Price", "Unused1" , "Unused2" , "Unused3" ]
		# Clear what is written on the labels by default
		for ControlName in self.labelNames:
			self.wTree.get_widget("lbl%s" % ControlName).set_text("")	

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
        	ItemDetails=self.parent.database.ProductDictionary(ItemID) 
        	for ControlName in self.labelNames:
			try:
				self.wTree.get_widget("lbl%s" % ControlName).set_text("%s" % ItemDetails[ControlName] or "")
			except:
				"""Nothing defined"""
		#Simply adds text to the buffer which is being shown in the textarea
		self.bufferDescription.set_text("%s" % ItemDetails["Description"],len("%s" % ItemDetails["Description"]))		
		#print ItemDetails

	def OnBasketClick(self, widget):
		"""Called when we want to take the product to the sale screen"""
		basketScreen=basket.Basket()

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
	