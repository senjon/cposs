"""Unit test for Mod_ProductData.py
"""

import Database.ProductData as ProductData
import unittest

class KnownValues(unittest.TestCase):
        fullyknownValues=((1,1, 'Payment Method','This is a payment method product. It enables barcode scanning of payments','Cash','','0.00')
                          ,(1,1, 'Payment Method','This is a payment method product. It enables barcode scanning of payments','Cash','','0.00'))
        knownValues = ((1, 'Payment Method')
                       ,(2, 'Payment Method')
                       ,(3, ''))
        def testGetItemFullExample(self):
                """GetItem should give a fully known result with a known input"""
                for ProductID,ItemID, Heading, Description, Detail1,Detail2, Price in self.fullyknownValues:
                        result = Mod_ProductData.ProductDictionary(ItemID)
                        self.assertEqual(ProductID, result["ProductID"])
                        self.assertEqual(ItemID, result["ItemID"])
                        self.assertEqual(Heading, result["Heading"])
                        self.assertEqual(Description, result["Description"])
                        self.assertEqual(Detail1, result["Detail1"])
                        self.assertEqual(Detail2, result["Detail2"])
                        self.assertEqual(Price, result["Price"])

        def testGetItemKnownValues(self):
                """GetItem should give a known header with a known input"""
                for ItemID, Heading in self.knownValues:
                        result = Mod_ProductData.ProductDictionary(ItemID)
                        self.assertEqual(Heading, result["Heading"])

class GetItemBadInput(unittest.TestCase):
        def testZero(self):
                """GetItem should fail with 0 input"""
                self.assertRaises(Mod_ProductData.OutOfRangeError, Mod_ProductData.ProductDictionary, 0)

        def testNegative(self):
                """GetItem should fail with negative input"""
                self.assertRaises(Mod_ProductData.OutOfRangeError, Mod_ProductData.ProductDictionary, -1)

        def testDecimal(self):
                """GetItem should fail with non-integer input"""
                self.assertRaises(Mod_ProductData.NotIntegerError, Mod_ProductData.ProductDictionary, 0.5)
class GetItemBadOutput(unittest.TestCase):
        def testNewBasketID(self):
                """Get a new BasketID"""
                result = Mod_ProductData.CreateBasket()
                self.assertEqual(result, int(result))
                
if __name__ == "__main__":
        unittest.main()
