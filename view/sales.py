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


class sales:
	"""Class for the sale screen"""	

	def __init__(self, parent, tab, basketid=None):
		"""Initiallise the Basket, load it up in gtk"""

		self.parent=parent

		#Set the Glade file
		self.gladefile = "glade/sales.glade"

		self.wTree = gtk.glade.XML(self.gladefile,"vbox1");
		_label = gtk.Label();
        	_label.set_text("Sales Screen")
        	
		tab.append_page(self.wTree.get_widget("vbox1"),_label);

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

		
		#Initiate the list (sale & return)
		self.initLists()
		
		

	def filter_func(self, model, iter,filtertype):
		# print "Quantity value for %s is %s" % (model.get_value(iter, self.Columns["ItemID"][0]) , model.get_value(iter, self.Columns["Quantity"][0]))
      		value = int(model.get_value(iter, self.Columns["Quantity"][0]))

		if filtertype=="posqty":
			if value>0:
				return True
		elif filtertype=="negqty":
			if value<0:
				return True		
		
	def filter_lessthan_value(self, model, iter,comparedto):
		print model.get_value(iter, self.Columns["Quantity"][0])
      		value = int(model.get_value(iter, self.Columns["Quantity"][0]))
		if value<comparedto:
			return True

	def FillBasket(self):
	  	"""Called to fill the sale list."""
		BasketDict=self.parent.database.ReturnBasket(self.basketid)
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
			widget.set_text("")
		if keypress in ["minus"]:
			self.AddToBasket(itemid,-self.qty)
			widget.set_text("")
		return True
			
	def AddToBasket(self,itemid,quantity):
			"""Called to add (or remove using negative qty) from the basket."""

			#Add item to database
			qty=self.parent.database.AddToBasket(itemid,quantity,self.basketid)
			print qty
			#Loop through all rows and update if necesary
			iter = self.lstSale_list.get_iter_root()
			RowsChanged=None
			while (iter):
				# Get the itemid of current row
				citemid = self.lstSale_list.get_value(iter, self.Columns["ItemID"][0])
				# If either of the ids are ints then convert to unicode
				print "%s == %s" % (unicode(itemid), unicode(citemid))
				if unicode(itemid)==unicode(citemid):
					# If we have a row with with the new item id then change the quantity to the new value
					self.lstSale_list.set(iter, self.Columns["Quantity"][0], qty)
					RowsChanged=1
				# Get the next iter
				iter = self.lstSale_list.iter_next(iter)
			if RowsChanged== None:
				# We didnt update a row in the previous loop, therefore we need to add the item to the list
				BasketDict=self.parent.database.ReturnBasket(self.basketid)
				for ItemDetail in BasketDict:
					if ItemDetail["ItemID"]==itemid:
						self.lstSale_list.append([ItemDetail["ItemID"],ItemDetail["Heading"],
				                                       ItemDetail["Detail1"],ItemDetail["Detail2"],
				                                       ItemDetail["Price"],ItemDetail["Qty"],ItemDetail["Qty"]])


	def OnComplete(self, widget):
		"""Called when sale is completed"""
		self.lstSale_list.set_value(1,2,"1")

	def initLists(self):
		#Get the treeView from the widget Tree
		self.lstSale = self.wTree.get_widget("lstSale")
		self.lstReturn = self.wTree.get_widget("lstReturn")
		
		


		ColumnNames=[_("ItemID"),_("Heading"),_("Detail1"),_("Detail2"),_("Price"),_("Quantity"),_("Total")]
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
	cposs = Basket()
	gtk.main()
