"""
cposs documentation
"""
from product import Product, Feature

class CompletedBasketsCannotBeChanged(Exception):
    pass


class Business(object):
    """
    The business class holds business level information
    """
    def __init__(self, name, establishments=None, \
                 categories=None, departments=None \
                 ):
        """
        Create a business with a string name
        """
        self.name = name
        self.establishments = []
        self.categories = []
        self.departments = []
        
    def __repr__(self):
        establishment_id = '' if self._product_id is None else \
                           ', _establishment_id=%s' % self._product_id
                           
        return "Business(%r, establishments=%r, categories=%r, departments=%r%s)" % \
                 (self.name, self.establishments, self.categories, self.departments, establishment_id)
    
class Establishment(object):
    """
    The Establishment class holds establishment level information
    """
    def __init__(self, address, stock=None, baskets=None, _establishment_id=None):
        """
        The minimum amount of information to create an establishment
         is it's address
        """
        self.address = address
        self.stock = stock or []
        self.baskets = baskets or []

    def __repr__(self):
        return "Establishment(%r, stock=%r, baskets=%r)" % \
                    (self.address, self.stock, self.baskets)

    
class Department(object):
    """
    The Department class holds establishment level information
    """
    def __init__(self, name, products=None):
        """
        The minimum amount of information to create a department
         is it's name
        """
        self.name = name
        self.products = products or []

    def __repr__(self):
        return "Department(%r, product_lines=%r)" % \
                    (self.name, self.product_lines)
                    
    def get_product(self, barcode):
        result = [product for product in self.products \
                 if product.barcode == barcode]
        if not result:
            raise ValueError('Product does not exist')
        return result[0]
 
        
if __name__ == "__main__":
    
    foo_bar = Business('FOO BAR')
    london_shop = Establishment('101 Oxford Street, London')
    
    jumpers = Department('Jumpers')
    foo_bar.departments.append(jumpers)
    foo_bar.establishments.append(london_shop)
    
    name = 'Hollister thin jumper'
    description = 'Longsleve thin jumper made by Hollister'
    price = 33.99
    product_59 = Product(59, name, description, price, 
                          [Feature('color', 'grey'), Feature('color', 'blue')])
    
    product_60 = Product(60, name, description, price, 
                          [Feature('color', 'red'), Feature('color', 'white')])
    import cposs.discount
    product_60.discounts_available.append(cposs.discount.NewPriceDiscount(product_60, None, 10))
    
    jumpers.products.extend([product_59, product_60])

    jumpers.get_product(60).save()
    jumpers.get_product(59).save()
    import cposs.basket
    a = cposs.basket.Basket(london_shop, None, [product_60, product_59], False)
    print a
    print a.total()