try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	print "PyGTK Not found or not at correct version"
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
        	_label.set_text(_("Settings"))
        	
		tab.append_page(self.wTree.get_widget("vbox1"),_label);

		self.wTab=self.wTree.get_widget("ntbkSettings")
		self.tab = {}

		self.tab_events={}
		self.tab_events['Hardware']={'on_valBarcodeASCII_changed' : self.on_valBarcodeASCII_changed}

		self.tab['Display']=self.LoadTab(self.wTab,_('Display Settings'),'Display')		
		self.tab['Hardware']=self.LoadTab(self.wTab,_('Hardware Settings'),'Hardware')
		
		self.tab_settings = {}
		self.tab_settings['Display'] = ['Name','Age','Car']
		self.tab_settings['Hardware'] = ['BarcodeASCII','Car2']

		self.LoadSettings()		


		#Create the dictionary of events and create them
		dic = {"on_Basket_destroy" : self.on_Quit, "on_cmdSave_clicked" : self.SaveSettings}
		self.wTree.signal_autoconnect(dic)
		
	def LoadTab(self,tabinstance,tablabel,tabname):
		display = gtk.glade.XML(self.gladefile,"tab%s" % tabname);
		_label = gtk.Label();
        	_label.set_text(tablabel)        	
		tabinstance.append_page(display.get_widget("tab" + tabname),_label);
		if self.tab_events.get(tabname,None) is not None:
			display.signal_autoconnect(self.tab_events[tabname])
		return display

	def LoadSettings(self):
		# Load the settings for each tab
		for name in self.tab:
			self._LoadSetting(self.tab[name],self.tab_settings[name])

	def _LoadSetting(self,wTree,settings):
		for value in settings:
			_widget = wTree.get_widget("val" + value)
			if _widget is not None: _widget.set_text(self.parent.mysettings.GetSetting(value))

	def SaveSettings(self, widget):
		# Load the settings for each tab
		for name in self.tab:
			self._SaveSetting(self.tab[name],self.tab_settings[name])
		self.parent.mysettings.SaveSettings()

	def _SaveSetting(self,wTree,settings):
		for value in settings:
			_widget = wTree.get_widget("val" + value)
			if _widget is not None: self.parent.mysettings.SetSetting(value,_widget.get_text())

	def on_Quit(self, widget):
		"""Called when the application is going to quit"""
		# Ask if we want to save the settings				
		gtk.main_quit()

	def on_valBarcodeASCII_changed(self, widget, event):
		"""Called when the field for the BarcodeASCII signout value is changed"""
		print event

if __name__ == "__main__":
	cposs = settings()
	gtk.main()
