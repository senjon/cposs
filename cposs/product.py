"""
Todo
"""
import xml.dom.minidom
import os

import cposs.config
import cposs.discount

def xml_getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc).strip()

class Product(object):
    """
    TODO
    
    """
    @staticmethod
    def get_product(barcode):
        path = cposs.config.PRODUCT_PATH + '/' + str(barcode) + '.xml'
        if not os.path.exists(path):
            raise ValueError('Barcode does not exist')
                    
        dom = xml.dom.minidom.parse(path)
        product_node = dom.getElementsByTagName("product")[0]
        description_node = product_node.getElementsByTagName("description")[0]
        description = xml_getText(description_node.childNodes)
        
        name = product_node.attributes['name'].value
        price = float(product_node.attributes['price'].value)
        _barcode = product_node.attributes['barcode'].value
        if barcode != int(_barcode):
            raise ValueError('The product file is inconsistent with the barcode in the file.')
        
        features = []
        features_node = dom.getElementsByTagName("features")[0]
        for feature_node in features_node.getElementsByTagName("feature"):
            name_node = feature_node.getElementsByTagName("name")[0]
            value_node = feature_node.getElementsByTagName("value")[0]
            feature_name = xml_getText(name_node.childNodes)
            feature_value = xml_getText(value_node.childNodes)
        
            features.append(Feature(feature_name, feature_value))
        
        product = Product(barcode, name, description, price, features)
        
        discounts_node = dom.getElementsByTagName("discounts")[0]
        discount_map = {'MoneyOffDiscount':cposs.discount.MoneyOffDiscount, 
                        'NewPriceDiscount':cposs.discount.NewPriceDiscount,
                        'PercentageDiscount':cposs.discount.PercentageDiscount,
                        }
        for discount_node in discounts_node.getElementsByTagName("discount"):
            type = discount_node.attributes['type'].value
            amount = float(discount_node.attributes['discount_ammount'].value)
            try:
                discount_class = discount_map[type]
            except KeyError:
                raise ValueError('Unknown discount type')
            
            product.discounts_available.append(discount_class(product, None, amount))

        return product    
    
    def __init__(self, barcode, name, description, rrp, features, discounts=None, _product_id=None ):
        """
        TODO
        """
        self.barcode = barcode
        self.name = name
        self.description = description
        self.rrp = rrp
        self.features = features
        self.discounts_available = discounts or []
        self._product_id = _product_id
        
    def __repr__(self):
        product_id = '' if self._product_id is None else ', _product_id=%s' % self._product_id 
        return "Product(%r, %r, %r, %r, %r, discounts=%r%r)" % \
                    (self.barcode, self.name, self.description, \
                     self.rrp, self.features, self.discounts_available, product_id)
    
    def price(self, establishment):
        (price, discount) = self.get_best_price_and_discount_used(establishment)
        return price 
        
    def get_best_price_and_discount_used(self, establishment=None):
        """
        Pick the best discount available
        establishment = None is equivalent to saying establishment = Any
        """
        best_price = self.rrp
        best_discount = None
        for discount in self.discounts_available:
            if discount.allowed(establishment) and discount.price < best_price:
                best_price = discount.price
                best_discount = discount
        return (best_price, best_discount)
    
    def save(self):
        """
        Save the appropriate XML
        """
    
        doc = xml.dom.minidom.Document()
        
        product = doc.createElement("product")
        doc.appendChild(product)
        
        product.setAttribute("barcode", str(self.barcode))
        
        product.setAttribute("name", str(self.name))
        
        product.setAttribute("price", str(self.rrp))
        
        description = doc.createElement("description")
        description_text = doc.createTextNode(self.description)
        description.appendChild(description_text)
        product.appendChild(description)

        features = doc.createElement("features")
        product.appendChild(features)
        for feature in self.features:
            features.appendChild(feature.xml(doc))
            
        discounts = doc.createElement("discounts")
        product.appendChild(discounts)
        for discount in self.discounts_available:
            discounts.appendChild(discount.xml(doc))
        
        f = open(cposs.config.PRODUCT_PATH + '/' + str(self.barcode) + '.xml', 'w')    
        f.write(doc.toprettyxml(indent="  "))
        f.close()


class Feature(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return 'Feature(%r, %r)' % (self.name, self.value)
    
    def xml(self, doc):
        feature = doc.createElement("feature")
        
        name = doc.createElement("name")
        name_text = doc.createTextNode(str(self.name))
        name.appendChild(name_text)
        
        value = doc.createElement("value")
        value_text = doc.createTextNode(str(self.value))
        value.appendChild(value_text)

        feature.appendChild(name)
        feature.appendChild(value)
        return feature

       
if __name__ == '__main__':
    p = Product.get_product(60)
    print p
    p.save()
    p = Product.get_product(60)
    print p