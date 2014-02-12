#!/usr/bin/env python

import datetime

import unittest
from JohnShoes import Shoe, Customer, Sale


class ShoeClassTestCase(unittest.TestCase):

    def setUp(self):
        self.size = 43
        self.color = 'fucsia'
        self.new_shoe = Shoe().new_shoe(self.size, self.color)

    def tearDown(self):
        self.new_shoe.delete()


    def test_new_shoe_returns_instance_new_shoe(self):
        self.assertIsInstance(self.new_shoe, Shoe)
        self.assertEquals(self.new_shoe.size, self.size)
        self.assertEquals(self.new_shoe.color, self.color)
        self.assertTrue(hasattr(self.new_shoe, '_id'))


    def test_call_save_on_already_saved_returns_none(self):
        self.assertEquals(self.new_shoe.save(), None)


    def test_get_by_size_returns_only_shoes_of_that_size(self):
        tiny_shoe = Shoe().new_shoe(30, self.color)
        duenas_shoe = Shoe().new_shoe(54, self.color)
        shoes_list = Shoe().get_by_size(self.size)
        for shoe in shoes_list:
            self.assertEqual(shoe.size, self.new_shoe.size)
            self.assertNotEqual(shoe.size, tiny_shoe.size)
            self.assertNotEqual(shoe.size, duenas_shoe.size)
        tiny_shoe.delete()
        duenas_shoe.delete()


    def test_get_by_color_returns_only_shoes_of_that_color(self):
        ugly_shoe = Shoe().new_shoe(self.size, 'silver')
        fancy_shoe = Shoe().new_shoe(self.size, 'gold')
        shoes_list = Shoe().get_by_color(self.color)
        for shoe in shoes_list:
            self.assertEqual(shoe.color, self.new_shoe.color)
            self.assertNotEqual(shoe.color, ugly_shoe.color)
            self.assertNotEqual(shoe.color, fancy_shoe.color)

        ugly_shoe.delete()
        fancy_shoe.delete()


    def test_get_by_id_returns_shoe_of_requested_id(self):
        requested_shoe = Shoe().get_by_id(self.new_shoe._id)
        self.assertEqual(requested_shoe._id, self.new_shoe._id)



class CustomerClassTestCase(unittest.TestCase):

    def setUp(self):
        self.name = "John's son"
        self.new_customer = Customer().new_customer(self.name)

    def tearDown(self):
        self.new_customer.delete()


    def test_new_customer_returns_instace_new_customer(self):
        self.assertIsInstance(self.new_customer, Customer)
        self.assertEquals(self.new_customer.name, self.name)
        self.assertTrue(hasattr(self.new_customer, '_id'))


    def test_call_save_on_already_saved_returns_none(self):
        self.assertEquals(self.new_customer.save(), None)


    def test_get_by_name_returns_only_customers_with_that_name(self):
        thief = Customer().new_customer('Mariano')
        ignorant = Customer().new_customer('Rajoy')
        customers_list = Customer().get_by_name(self.name)
        for customer in customers_list:
            self.assertEqual(customer.name, self.new_customer.name)
            self.assertNotEqual(customer.name, thief.name)
            self.assertNotEqual(customer.name, ignorant.name)

        thief.delete()
        ignorant.delete()


    def test_get_by_id_returns_customer_of_requested_id(self):
        requested_customer = Customer().get_by_id(self.new_customer._id)
        self.assertEqual(requested_customer._id, self.new_customer._id)



class SaleClassTestCase(unittest.TestCase):

    def setUp(self):
        self.new_shoe = Shoe().new_shoe(32, 'white')
        self.new_customer = Customer().new_customer('Arnau')
        self.shoe_id = self.new_shoe._id
        self.customer_id = self.new_customer._id
        self.new_sale = Sale().new_sale(self.shoe_id, self.customer_id)

    def tearDown(self):
        Sale().delete_by_id(self.new_sale[3])
        self.new_shoe.delete()
        self.new_customer.delete()


    def test_add_new_sale_returns_tuple_new_sale(self):
        self.assertIsInstance(self.new_sale, tuple)
        self.assertEquals(self.new_sale[0], self.new_shoe._id)
        self.assertEquals(self.new_sale[1], self.new_customer._id)



if __name__ == '__main__':
    unittest.main(verbosity=3)

