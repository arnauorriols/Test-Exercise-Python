#!/usr/bin/env python

import datetime

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

class baseModel(object):
    """ Base class for model objects. Child class must add db_collection attribute """

    client = MongoClient()
    js_db = client.john_shoes
    counters = js_db.counters

    def save(self):
        try:
            new_entry = self.__dict__.copy()
            del new_entry['db_collection']
            return self.db_collection.insert(new_entry)
        except DuplicateKeyError:
            # Update is not still implemented
            pass

    def getIndex(self, collection):
        return self.counters.find_and_modify(
                                                {'_id' : collection},
                                                {'$inc' : {'count':1}},
                                                new = True
                                            )['count']

    def get_by_id(self, _id):
        return self.db_collection.find_one({'_id' : _id })

    def delete_by_id(self, _id):
        self.db_collection.remove({'_id' : _id})

    def delete(self):
        try:
            self.delete_by_id(self._id)
        except:
            pass



class Shoe(baseModel):

    def __init__(self):
        self.db_collection = self.js_db.shoes
        if self.counters.find({'_id' : 'shoe'}).count() == 0:
            # Create id generator collection
            self.counters.insert({ '_id' : 'shoe', 'count' : 0 })

    def new_shoe(self, size, color, _id=None):
        """
        Called to retrieve another instance of Shoe. If _id is not specified,
        creates a new shoe, with a new id.

        """

        self.size = size
        self.color = color

        if not _id:
            self._id = self.getIndex('shoe')
            self.save()
        else:
            self._id = _id
        return self


    def get_by_size(self, value):
        return [self.new_shoe(**found_shoe)
                    for found_shoe in self.db_collection.find({ 'size' : value })]


    def get_by_color(self, value):
        return [self.new_shoe(**found_shoe)
                    for found_shoe in self.db_collection.find({ 'color' : value })]


    def get_by_id(self, _id):
        return self.new_shoe(**super(Shoe, self).get_by_id(_id))



class Customer(baseModel):

    def __init__(self):
        self.db_collection = self.js_db.customers
        if self.counters.find({'_id' : 'customer'}).count() == 0:
            self.counters.insert({ '_id' : 'customer', 'count' : 0 })

    def new_customer(self, name, _id=None):
        self.name = name
        if not _id:
            self._id = self.getIndex('customer')
            self.save()
        else:
            self._id = _id

        return self


    def get_by_name(self, value):
        return [self.new_customer(**found_customer)
                    for found_customer in self.db_collection.find({ 'name' : value })]


    def get_by_id(self, _id):
        return self.new_customer(**super(Customer, self).get_by_id(_id))



class Sale(baseModel):

    def __init__(self):
        self.db_collection = self.js_db.sales

    def new_sale(self, shoe_id, customer_id):
        """
        Returns tuple (shoe_id, customer_id, sale's datetime, sale's id)
        instead of Sale instance.

        """

        self.shoe_id = shoe_id
        self.customer_id = customer_id
        self._id = ObjectId()
        self.date = self._id.generation_time
        self.save()

        return (self.shoe_id, self.customer_id, self.date, self._id)


    def get_sales(self, from_date, to_date):
        """ Returns list of sale's tuples between the two datetimes passed as arguments """

        return [(sale['shoe_id'], sale['customer_id'], sale['_id'])
                                    for sale in self.db_collection.find({
                                                 'date': {
                                                            '$gte' : from_date,
                                                            '$lt' : to_date
                                                         }
                                                 })]
