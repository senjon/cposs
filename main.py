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
	print "Import error, cposs cannot start. Check your dependencies."
	sys.exit(1)

try:
	import home.home as home
	import sales.sales as sales
	import Database.ProductData as ProductData
except:
	print "Some modules could not be loaded."

FILE_EXT = "cposs"
APP_NAME = "cposs"


class cposs:
	"""The cposs class"""

	def __init__(self):
		
		self.ProductData=ProductData

		# Set the project file
		self.project_file = ""

		#Set the Glade file
		self.gladefile = "Glade/main.glade"
		self.gladefile_common = "Glade/common.glade"

		self.wTree = gtk.glade.XML(self.gladefile, "Main")
		self.win = self.wTree.get_widget("Main")
		self.win.maximize()
		self.wTab = self.wTree.get_widget("tabs")
		
		self.homescreen = home.home(self,self.wTab)

		_xml = gtk.glade.XML("Glade/sales.glade","vbox1");
		_label = gtk.Label();
        	_label.set_text("Sales Screen")
        	self.wTab.append_page(_xml.get_widget("vbox1"),_label);

	
		#Create the dictionary of events and create them
		dic = {	"on_Main_destroy" : self.on_Quit,	
			"on_button2_clicked" : self.on_Quit }
		self.wTree.signal_autoconnect(dic)
	
	def on_Quit(self, widget):
		"""Called when the application is going to quit"""
		gtk.main_quit()
	def printme(self):
		"""Print to test"""
		print "Hello, I have accessed you from the parent.";

if __name__ == "__main__":
	cposs = cposs()
	
	gtk.main()
	
