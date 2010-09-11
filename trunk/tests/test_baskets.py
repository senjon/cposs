    thin_jumper = ProductLine('Hollister thin jumper', 'Longsleve thin jumper made by Hollister', 33.99)
    product_59 = Product(59, [Feature('color', 'grey'), Feature('color', 'blue')])
    product_60 = Product(60, [Feature('color', 'navy')])
    
    thin_jumper.add_product(product_59)
    thin_jumper.add_product(product_60)
    
    jumpers.product_lines.append(thin_jumper)

    print jumpers.get_product(60)
    
    a = Basket(None, 'foo', False)
    a.customer = 'a'