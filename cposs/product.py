"""
Todo
"""
import xml.dom.minidom
import os

import cposs.config

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
        name_node = product_node.getElementsByTagName("name")[0]
        name = xml_getText(name_node.childNodes)
        
        price = product_node.getElementsByTagName("name")[0]
        discounts = xml_getText(name_node.childNodes)
        
        features = []
        features_node = dom.getElementsByTagName("features")[0]
        for feature_node in features_node.getElementsByTagName("feature"):
            name_node = feature_node.getElementsByTagName("name")[0]
            value_node = feature_node.getElementsByTagName("value")[0]
            feature_name = xml_getText(name_node.childNodes)
            feature_value = xml_getText(value_node.childNodes)
        
            features.append(Feature(feature_name, feature_value))
        
        discounts = []
        discounts_node = dom.getElementsByTagName("discounts")[0]
        for discount_node in discounts_node.getElementsByTagName("discount"):
            type_node = discount_node.getElementsByTagName("type")[0]
            ammount_node = discount_node.getElementsByTagName("discount_ammount")[0]
        
            # discounts.append(cposs.discount.Discount(feature_name, feature_value))

            
        return Product(barcode, name, None, 0, features)
    
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