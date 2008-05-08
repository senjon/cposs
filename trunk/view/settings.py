try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	print "PyGTK Not found or not at correct level"
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


class settings:
	"""Class for the sale screen"""	

	def __init__(self, parent, tab, basketid=None):
		"""Initiallise the Basket, load it up in gtk"""

		self.parent=parent

		#Set the Glade file
		self.gladefile = "glade/settings.glade"

		self.wTree = gtk.glade.XML(self.gladefile,"vbox1");
		_label = gtk.Label();
        	_label.set_text("Settings")
        	
		tab.append_page(self.wTree.get_widget("vbox1"),_label);

		self.wTab=self.wTree.get_widget("ntbkSettings")
		self.tab_display=self.LoadTab(self.wTab,'Display')		
		self.tab_connectivity=self.LoadTab(self.wTab,'Connectivity')

		
		self.tab_display_settings = ['Name','Age','Car']
		self.tab_connectivity_settings = ['Name3','Car2']
		self.LoadSettings()		


		#Create the dictionary of events and create them
		dic = {"on_Basket_destroy" : self.on_Quit, "on_cmdSave_clicked" : self.SaveSettings}
		self.wTree.signal_autoconnect(dic)
		
	def LoadTab(self,SettingsTab,tabname):
		display = gtk.glade.XML(self.gladefile,"tab%s" % tabname);
		_label = gtk.Label();
        	_label.set_text(tabname)        	
		SettingsTab.append_page(display.get_widget("tab" + tabname),_label);
		return display

	def LoadSettings(self):
		# Load the settings for each tab
		self._LoadSetting(self.tab_display,self.tab_display_settings)
		self._LoadSetting(self.tab_connectivity,self.tab_connectivity_settings)

	def _LoadSetting(self,wTree,settings):
		for value in settings:
			_widget = wTree.get_widget("val" + value)
			if _widget is not None: _widget.set_text(self.parent.mysettings.GetSetting(value))

	def SaveSettings(self, widget):
		# Load the settings for each tab
		self._SaveSetting(self.tab_display,self.tab_display_settings)
		self._SaveSetting(self.tab_connectivity,self.tab_connectivity_settings)
		self.parent.mysettings.SaveSettings()

	def _SaveSetting(self,wTree,settings):
		for value in settings:
			_widget = wTree.get_widget("val" + value)
			if _widget is not None: self.parent.mysettings.SetSetting(value,_widget.get_text())

	def on_Quit(self, widget):
		"""Called when the application is going to quit"""
		# Ask if we want to save the settings		
		
		gtk.main_quit()

if __name__ == "__main__":
	cposs = settings()
	gtk.main()
