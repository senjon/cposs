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
	from os.path import abspath, dirname, join, pardir

	import locale
	import gettext
except:
	print "Import error, cposs cannot start. Check your dependencies."
	sys.exit(1)
import view.home as home
import view.sales as sales
import view.settings as settings
import controller.settings as ctrlsettings
import controller.ProductData as ctrlproductdata



FILE_EXT = "cposs"
APP_NAME = "cposs"


#Translation stuff



class cposs:
	"""The cposs class"""

	def __init__(self):
		import __builtin__
		__builtin__._ = cposs.trans(self)


		self.database=ctrlproductdata
		self.mysettings=ctrlsettings.Settings()

		# Set the project file
		self.project_file = ""

		#Set the Glade file
		self.gladefile = "glade/main.glade"
		self.gladefile_common = "glade/common.glade"

		self.wTree = gtk.glade.XML(self.gladefile, "Main")
		self.win = self.wTree.get_widget("Main")
		self.win.maximize()
		self.wTab = self.wTree.get_widget("tabs")
		
		self.settings = settings.settings(self,self.wTab)

		self.home = home.home(self,self.wTab)
		self.sales = sales.sales(self,self.wTab)
		self.sales2 = sales.sales(self,self.wTab,6) # syntax for calling a specific BasketID

	
		#Create the dictionary of events and create them
		dic = {	"on_Main_destroy" : self.on_Quit,
			"on_button1_clicked" : self.ViewSales,	
			"on_button2_clicked" : self.on_Quit }
		self.wTree.signal_autoconnect(dic)

	def ViewSales(self, widget):
		"""View Sales"""
		self.wTab.next_page()

	def on_Quit(self, widget):
		"""Called when the application is going to quit"""
		gtk.main_quit()

	def trans(self):


		#Translation stuff

		#Get the local directory since we are not installing anything
		self.local_path = os.path.realpath(os.path.dirname(sys.argv[0])) + "/data/languages/"
		# Init the list of languages to support
		langs = []
		#Check the default locale
		lc, encoding = locale.getdefaultlocale()
		if (lc):
			#If we have a default, it's the first in the list
			langs = [lc]
		# Now lets get all of the supported languages on the system
		language = os.environ.get('LANGUAGE', None)
		if (language):
			"""langage comes back something like en_CA:en_US:en_GB:en
			on linuxy systems, on Win32 it's nothing, so we need to
			split it up into a list"""
			langs += language.split(":")
		"""Now add on to the back of the list the translations that we
		know that we have, our defaults"""
		langs += ["en_CA", "en_GB"]

		"""Now langs is a list of all of the languages that we are going
		to try to use.  First we check the default, then what the system
		told us, and finally the 'known' list"""
	
		for module in (gettext, gtk.glade):
		     module.bindtextdomain(APP_NAME, self.local_path)
		     module.textdomain(APP_NAME)

		gettext.bindtextdomain(APP_NAME, self.local_path)
		gettext.textdomain(APP_NAME)
		gtk.glade.bindtextdomain(APP_NAME, self.local_path)
		gtk.glade.textdomain(APP_NAME)

		# Get the language to use
		self.lang = gettext.translation(APP_NAME, self.local_path
			, languages=langs, fallback = True)
		"""Install the language, map _() (which we marked our
		strings to translate with) to self.lang.gettext() which will
		translate them."""
		
		return self.lang.gettext


if __name__ == "__main__":
	cposs = cposs()
	gtk.main()
	
