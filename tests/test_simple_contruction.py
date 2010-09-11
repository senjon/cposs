    DAISY = Business('Lazy Daisy')
    DAISY_RHOS_SHOP = Establishment('79 The Promenade')
    print DAISY_RHOS_SHOP
    SHOES = Department('Shoes')
    print SHOES
    DAISY.departments.append(SHOES)
    DAISY.establishments.append(DAISY_RHOS_SHOP)
    print DAISY
    DAISY_RHOS_SHOP.stock.append('foo')
    print DAISY
    
    DAISY_RHOS_SHOP.stock.append('foo')
    
    Jumper = ProductLine('Jumper', 'Nice woolen jumper', 3.99)
    product_59 = Product(59, [Feature('color', 'red')])
    product_60 = Product(60, [Feature('color', 'black')])
    
    Jumper.add_product(product_59)
    Jumper.add_product(product_60)
    
    print product_59
    print Jumper