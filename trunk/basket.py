try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	print "PyGTK Not found or not at correct level"
try:
	import sys
	import Database.ProductData as ProductData
	import gtk
	import gtk.glade
	import gobject
	import logging
	import shelve
	import os
	import locale
	import gettext
except:
	print "Import error, epos cannot start. Check your dependencies."
	sys.exit(1)


class Basket:
	"""Class for the sale screen"""	

	def __init__(self, basketid=None):
		"""Initiallise the Basket, load it up in gtk"""

		#setup the glade file
		self.gladefile = "Glade/sales.glade"
		#load the window from the glade file
		self.wTree = gtk.glade.XML(self.gladefile, "Basket")
		#Get the actual window widget
		self.win = self.wTree.get_widget("Basket")
		#maximise it
		self.win.maximize()
		#self.win.fullscreen()

		#check to see if the basketid has been passed
		self.basketid = basketid or "2"
		
		#This vairable is for when we add a quantity of a product (++TODO a widget will allow us to change this value before we scan)
		self.qty=1
		
		#Create the dictionary of events and create them
		dic = {"on_Basket_destroy" : self.on_Quit, "on_btnComplete_clicked" : self.OnComplete}
		self.wTree.signal_autoconnect(dic)
		
		#Problems automatically assigning keypressevent to gtkentry widget, use code below instead.		
		txtBarcode = self.wTree.get_widget("txtBarcode")
        	txtBarcode.connect("key_press_event",self.OnBarcodeChange)

		
		#Initiate a database connection
		self.db=ProductData

		#Initiate the list (sale & return)
		self.initLists()
		
		

	def filter_func(self, model, iter,filtertype):
		value = int(model.get_value(iter, 5))
		if filtertype=="posqty":
			if value>0:
				return True
		elif filtertype=="negqty":
			if value<0:
				return True		
		
	def filter_lessthan_value(self, model, iter,comparedto):
      		value = int(model.get_value(iter, 5))
		if value<comparedto:
			return True

	def FillBasket(self):
	  	"""Called to fill the sale list."""
		BasketDict=self.db.ReturnBasket(self.basketid)
		for ItemDetail in BasketDict:
			self.lstSale_list.append([ItemDetail["ItemID"],ItemDetail["Heading"],
                                                       ItemDetail["Detail1"],ItemDetail["Detail2"],
                                                       ItemDetail["Price"],ItemDetail["Qty"],ItemDetail["Qty"]])

	def CreateColumn(self, title, columnId=0,width=100):
		"""Creates + Returnes a column with the styling specified - the column still needs to be added to the liststore"""

		column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=columnId)
		column.set_resizable(False)
		column.set_max_width(width)
		column.set_min_width(width)
		column.set_alignment(0.5)
		#column.set_sort_column_id(columnId)  #If you want the fields to be sortable
		#column.set_sort_column_id(3)
		return column

	def OnBarcodeChange(self, widget, event=None):
		"""Called when the user types in the text area"""
		keypress=gtk.gdk.keyval_name (event.keyval)
	   	#print "Key pressed in %s : %s" % (widget.name,keypress)
	   	#print "Value of %s before : %s" % (widget.name,widget.get_text())
		itemid=int(widget.get_text())

		if keypress in ["plus"]:
			self.AddToBasket(itemid,self.qty)
		if keypress in ["minus"]:
			self.AddToBasket(itemid,-self.qty)
			
	def AddToBasket(self,itemid,quantity):
			"""Called to add (or remove using negative qty) from the basket."""

			#Add item to database
			qty=self.db.AddToBasket(itemid,quantity,self.basketid)
			print qty
			#Loop through all rows and update if necesary
			iter = self.lstSale_list.get_iter_root()
			while (iter):
				# Get the itemid of current row
				citemid = int(self.lstSale_list.get_value(iter, self.Columns["ItemID"][0]))
				if itemid==citemid:
					cqty = int(self.lstSale_list.get_value(iter, self.Columns["Quantity"][0]))
					citemid = self.lstSale_list.set_value(iter, self.Columns["Quantity"][0], qty)
				# Get the next iter
				iter = self.lstSale_list.iter_next(iter)

	def OnComplete(self, widget):
		"""Called when sale is completed"""
		self.lstSale_list.set_value(1,2,"1")

	def initLists(self):
		#Get the treeView from the widget Tree
		self.lstSale = self.wTree.get_widget("lstSale")
		self.lstReturn = self.wTree.get_widget("lstReturn")
		
		ColumnNames=["ItemID","Heading","Detail1","Detail2","Price","Quantity","Total"]
		#self.ColumnNamesTranslated=["ItemID","Heading","Detail1","Detail2","Price","Quantity","Total"]
		ColumnIDs=[0,1,2,3,4,5]
		#Don't need to store the widths to the class
		ColumnWidths=[100,200,150,150,150,100]

		#Initiate the Columns variable
		self.Columns={}

		for Name,ColumnID,Width in zip(ColumnNames,ColumnIDs,ColumnWidths):
			#Populate the columns variable so that we can find the ColumnIDs later
			self.Columns[Name]=[ColumnID,Name]

			column=self.CreateColumn(Name,ColumnID,Width)			
			self.lstSale.append_column(column)
			#repeating this command, causes an error otherwise
			column=self.CreateColumn(Name,ColumnID,Width)
			self.lstReturn.append_column(column)

		
		#Create the listStore Model to use with the saleslist
		self.lstSale_list = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,  gobject.TYPE_STRING, gobject.TYPE_STRING )

		#Populate lists before creating the filters to save the machine some work
		self.FillBasket()
		
		#Create filters (positive & negative quantities)
  		positivefilter = self.lstSale_list.filter_new()
  		positivefilter.set_visible_func(self.filter_func,"posqty")
  		negativefilter = self.lstSale_list.filter_new()
  		negativefilter.set_visible_func(self.filter_func,"negqty")

		#Attach the model to the treeView
		self.lstSale.set_model(positivefilter)
		self.lstReturn.set_model(negativefilter)

	def on_Quit(self, widget):
		"""Called when the application is going to quit"""
		gtk.main_quit()

if __name__ == "__main__":
	epos = Basket()
	gtk.main()
