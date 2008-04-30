import re

class Product:
	"""This class represents all the Product information"""

	def __init__(self,result):
		self.ProductID = result[0]
		self.ItemID = result[1]
		self.Heading = result[2]
		self.Description = result[3]
		self.Detail1= result[4]
		self.Detail2= result[5]
		self.Price= result[6]

	def list(self):
		"""This function returns a dictionary made up of the
		Product information."""
		return {'ProductID':self.ProductID,
			'ItemID':self.ItemID, 
			'Heading':self.Heading, 
			'Description':self.Description, 
			'Detail1':self.Detail1,
			'Detail2':self.Detail2,
			'Price':self.Price}

class DatabaseConnect:
    """Connects to the database and keeps the connection open
    """
    def __init__(self):
        import MySQLdb
        DatabaseHost="localhost"
        DatabaseUsername="cposs"
        DatabasePassword="cposs"
        DatabaseName="cposs"
        self.db=MySQLdb.connect(DatabaseHost,DatabaseUsername, DatabasePassword, DatabaseName)
        self.cursor=self.db.cursor()


def FindBarcode(ItemID):
		"""Called when the user changes the barcode value"""
		return "Works :-)"

def ProductDictionary(ItemID):
    """Gets the product data of a given ItemID from the database
    """

    db=DatabaseConnect()
    
    #Make the SQL query
    SQLqry="""
    SELECT a.ProductID, ItemID, Heading, Description, Detail1, Detail2, Price
    FROM products as a LEFT JOIN products_sub as b
    ON a.ProductID = b.ProductID WHERE ItemID='%s'
    LIMIT 1
    """ % ItemID

    # execute SQL statement
    db.cursor.execute(SQLqry)

    # get the resultset as a tuple
    result = db.cursor.fetchall()

    #Close the database
    db.db.close()
    
    prod=Product(result[0])
    return prod.list()
   

def ReturnBasket(BasketID):
    """Returns an existing basket and it's contents
    """
    db=DatabaseConnect()
    
    #Make the SQL query
    SQLqry="""
    SELECT a.BasketID, b.ItemID, b.Qty, d.ProductID, d.Heading, d.Price, c.Detail1, c.Detail2
    FROM basket as a
    LEFT JOIN basket_sub as b
    ON a.BasketID=b.BasketID
    LEFT JOIN products_sub as c
    ON b.ItemID=c.ItemID
    LEFT JOIN products as d
    ON c.ProductID=d.ProductID
    WHERE a.BasketID='%s'
    LIMIT 100
    """ % BasketID

    # execute SQL statement
    db.cursor.execute(SQLqry)

    # get the resultset as a tuple
    result = db.cursor.fetchall()

    #Close the database
    db.db.close()
    returnDict=[]
    #Return what we found
    for BasketID, ItemID, Qty, ProductID, Heading, Price, Detail1, Detail2 in result:
             returnDict.append({'BasketID': BasketID,
              'ItemID': ItemID or '0',
            'Qty': Qty or '0',
            'ProductID': ProductID or '',
            'Heading':Heading or '',
            #'Price': '%0.2f' % int(Price) or '0.00',
            'Price': '0.00',            
	    'Detail1': Detail1 or '',
            'Detail2': Detail2 or ''
            }
            )
    return returnDict


def AddToBasket(ItemID,Qty=1,BasketID=0):
    """Adds a product to the shopping basket given an ItemID and optionally a quantity and/or BasketID
    """

    db=DatabaseConnect()
    
    
    #Make the SQL query
    SQLqry="""
    	SELECT Qty, Price FROM basket_sub
	LEFT JOIN products_sub ON basket_sub.ItemID=products_sub.ItemID 
	LEFT JOIN products ON products.ProductID=products_sub.ProductID 
	WHERE BasketID='%s' AND products_sub.ItemID='%s' 
	LIMIT 1;
    """ % (BasketID, ItemID)

    cur1=db.db.cursor()
    
    # execute SQL statement
    cur1.execute(SQLqry)
    row = cur1.fetchone()
    
    if row == None:
        print "Item Doesn't exist in Basket"
        SQLqry="""INSERT INTO basket_sub (`BasketID`, `ItemID`, `Qty`) VALUES ('%s','%s','%s')
        """ % (BasketID, ItemID, Qty)

    elif row[0]<0:
        #print "Item is being returned as there was a negative qty"
        SQLqry="""UPDATE basket_sub Set `Qty`=`Qty` + %s WHERE BasketID=%s AND ItemID=%s
        """ % (Qty, BasketID, ItemID)
        
    elif row[0]==0:
        #print "None of this item in the Basket"
        SQLqry="""UPDATE basket_sub Set `Qty`=`Qty` + %s WHERE BasketID=%s AND ItemID=%s
        """ % (Qty, BasketID, ItemID)
    else:
        print "We have a positive qty"
        SQLqry="""UPDATE basket_sub Set `Qty`=`Qty` + %s WHERE BasketID=%s AND ItemID=%s
        """ % (Qty, BasketID, ItemID)

    cur1.close()

    cur2=db.db.cursor()
    #Execute the new Qry
    db.cursor.execute(SQLqry)
    
    #Commit and Close the database
    cur2.close()
    db.db.commit()

    

