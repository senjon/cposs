Core data types
===============

.. graphviz::

	digraph G {
        fontname = "Bitstream Vera Sans"
        fontsize = 8

        node [
                fontname = "Bitstream Vera Sans"
                fontsize = 8
                shape = "record"
        ]

        edge [
                fontname = "Bitstream Vera Sans"
                fontsize = 8
		dir = none
        ]

        Business [
                label = "{Business|+ name}"
        ]

        Establishment [
                label = "{Establishment|+ retail (bool)\n+ warehouse (bool)\n+ address}"
        ]


        Category [
                label = "{Category|+ name}"
        ]

        Department [
                label = "{Department|+ name}"
        ]

        Basket [
                label = "{Basket|+ paid\n+ customer\n+ total}"
        ]

        ProductLineCombinationDiscount [
                label = "{ProductLineCombinationDiscount|}"
        ]

        ProductLine [
                label = "{ProductLine|+ name\n+ description\n+price}"
        ]

        ProductLineDiscount [
                label = "{ProductLineDiscount|+ name\n+ conditions (establishment,\l department, category)}"
        ]

        BasketProduct [
                label = "{BasketProduct|+ price}"
        ]


        Stock [
                label = "{Stock|+ barcode\n+ quantity\n+ establishment}"
        ]

        Product [
                label = "{Product|+ barcode (list)\n+ details (color, shape, size)}"
        ]

	# Containment
        edge [
                arrowhead = "normal"
                arrowtail = "diamond"	
        ]

	Establishment -> Basket
	Establishment -> Stock
	Business -> Establishment
	Business -> Category
	Business -> Department
	Department -> ProductLine
	Basket -> BasketProduct
	ProductLine -> Product
	ProductLine -> ProductLineDiscount
	Business -> ProductLineCombinationDiscount

        edge [
                arrowhead = "none"
                arrowtail = "odiamond"
        ]

	# Association links
	Stock -> Product
	Category -> ProductLine
	BasketProduct -> Product
	BasketProduct -> ProductLineDiscount
	Basket -> ProductLineCombinationDiscount	
	ProductLineCombinationDiscount -> ProductLine

	}


ProductLine
^^^^^^^^^^^

Product
^^^^^^^

Basket
^^^^^^

Category
^^^^^^^^
