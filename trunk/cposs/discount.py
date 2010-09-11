"""
cposs documentation
"""


class Discount(object):
    """
    """        
    def __init__(self, product, establishment_conditions, discount_ammount):
        self.product_rrp = product.rrp
        self.product_barcode = product.barcode
        self.establishment_conditions = establishment_conditions
        self.discount_ammount = discount_ammount
        
    def allowed(self, establishment):
        # TODO, consider conditions of allowed discounts
        return True
    
    @property
    def price(self):
        raise NotImplementedError()
    
    def xml(self, doc):
        discount = doc.createElement("discount")
        
        discount.setAttribute("type", str(self.__class__.__name__))
        discount.setAttribute("discount_ammount", str(self.discount_ammount))
        
        return discount
    

class MoneyOffDiscount(Discount):
    """
    """
    @property
    def price(self):
        return self.product_rrp - self.discount_ammount
    

class NewPriceDiscount(Discount):
    """
    """
    @property
    def price(self):
        return self.discount_ammount
    

class PercentageDiscount(Discount):
    """
    """
    @property
    def price(self):
        return self.product_rrp / 100 * (100-self.discount_ammount)
