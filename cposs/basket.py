"""
cposs documentation
"""


class CompletedBasketsCannotBeChanged(Exception):
    pass


class Basket(object):
    _complete=False
    def __init__(self, establishment, customer, basket_products=None, complete=False):
        self.establishment = establishment
        self.customer = customer
        self.basket_products = basket_products
        self._complete = complete
    
    def complete(self):
        for i, product in enumerate(self.basket_products):
            price, discount = product.get_best_price_and_discount_used(self.establishment)
            self.basket_products[i] = BasketProduct(price.barcode, product.rrp, discount)
        self._complete = True
        
    
    def __setattr__(self, name, value):
        """
        Baskets which have been completed cannot be changed...
        """
        if self._complete:
            raise CompletedBasketsCannotBeChanged()
        object.__setattr__(self, name, value)
    
    def __repr__(self):
        return 'Basket(%r, %r, %r, %r)' % (self.establishment, \
                                           self.customer, \
                                           self.basket_products, \
                                           self._complete) 

    def total(self):
        total = 0.0
        for bp in self.basket_products:
            print repr(bp.price(self.establishment))
            total += bp.price(self.establishment)
        return total
              

class BasketProduct(object):
    @staticmethod
    def create_basket_product(product, establishment):
        price, discount = product.get_best_price_and_discount_used()
        return BasketProduct(product.barcode, product.rrp, discount)
        
    _complete=False
    def __init__(self, barcode, rrp, discount, complete=False):
        self.barcode = barcode
        self.rrp = rrp
        self.discount = discount
        self._complete = complete
        
    def __setattr__(self, name, value):
        """
        Baskets which have been completed cannot be changed...
        """
        if self._complete:
            raise CompletedBasketsCannotBeChanged()
        object.__setattr__(self, name, value)
    
    def __repr__(self):
        return 'Basket(%r, %s, %r, _complete=%s)' % (self.barcode, \
                                   self.rrp, \
                                   self.discount, \
                                   self._complete) 

    def price(self, establishment):
        if not self.discount:
            return self.rrp
        else:
            return self.discount.price
            
        
if __name__ == "__main__":
    import cposs
    shop = cposs.Establishment('FOO BAR')
    
    p = cposs.Product.get_product(60)
    a = Basket(shop, None, [p])
    print a
    print a.total()