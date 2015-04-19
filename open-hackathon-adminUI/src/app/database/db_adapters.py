# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------------
# Copyright (c) Microsoft Open Technologies (Shanghai) Co. Ltd.  All rights reserved.
#  
# The MIT License (MIT)
#  
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#  
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#  
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------------

class DBAdapter(object):
    def __init__(self, db):
        self.db = db


class SQLAlchemyAdapter(DBAdapter):
    def __init__(self, db):
        super(SQLAlchemyAdapter, self).__init__(db)

    def get_object(self, ObjectClass, id):
        """ Retrieve one object specified by the primary key 'pk' """
        return ObjectClass.query.get(id)

    def find_all_objects(self, ObjectClass, *criterion):
        return ObjectClass.query.filter(*criterion).all()

    def find_all_objects_by(self, ObjectClass, **kwargs):
        return ObjectClass.query.filter_by(**kwargs).all()

    def count(self, ObjectClass, **kwargs):
        """ Retrieve all objects matching the case sensitive filters in 'kwargs'. """

        # Convert each name/value pair in 'kwargs' into a filter
        query = ObjectClass.query
        for field_name, field_value in kwargs.items():

            # Make sure that ObjectClass has a 'field_name' property
            field = getattr(ObjectClass, field_name, None)
            if field is None:
                raise KeyError(
                    "SQLAlchemyAdapter.find_first_object(): Class '%s' has no field '%s'." % (ObjectClass, field_name))

            # Add a filter to the query
            query = query.filter(field.in_((field_value,)))

        # Execute query
        return query.count()

    def filter(self, ObjectClass, *criterion):
        query = ObjectClass.query
        return query.filter(*criterion)

    def filter_by(self, ObjectClass, **kwargs):
        query = ObjectClass.query
        return query.filter_by(**kwargs)

    def find_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object matching the case sensitive filters in 'kwargs'. """

        # Convert each name/value pair in 'kwargs' into a filter
        query = ObjectClass.query
        for field_name, field_value in kwargs.items():

            # Make sure that ObjectClass has a 'field_name' property
            field = getattr(ObjectClass, field_name, None)
            if field is None:
                raise KeyError(
                    "SQLAlchemyAdapter.find_first_object(): Class '%s' has no field '%s'." % (ObjectClass, field_name))

            # Add a case sensitive filter to the query
            query = query.filter(field == field_value)  # case sensitive!!

        # Execute query
        return query.first()

    def ifind_first_object(self, ObjectClass, **kwargs):
        """ Retrieve the first object matching the case insensitive filters in 'kwargs'. """

        # Convert each name/value pair in 'kwargs' into a filter
        query = ObjectClass.query
        for field_name, field_value in kwargs.items():

            # Make sure that ObjectClass has a 'field_name' property
            field = getattr(ObjectClass, field_name, None)
            if field is None:
                raise KeyError(
                    "SQLAlchemyAdapter.find_first_object(): Class '%s' has no field '%s'." % (ObjectClass, field_name))

            # Add a case sensitive filter to the query
            query = query.filter(field.ilike(field_value))  # case INsensitive!!

        # Execute query
        return query.first()

    def add_object(self, inst):
        self.db.session.add(inst)

    def add_object_kwargs(self, ObjectClass, **kwargs):
        """ Add an object of class 'ObjectClass' with fields and values specified in '**kwargs'. """
        object = ObjectClass(**kwargs)
        self.db.session.add(object)
        return object

    def update_object(self, object, **kwargs):
        """ Update object 'object' with the fields and values specified in '**kwargs'. """
        for key, value in kwargs.items():
            if hasattr(object, key):
                setattr(object, key, value)
            else:
                raise KeyError("Object '%s' has no field '%s'." % (type(object), key))

    def delete_object(self, object):
        """ Delete object 'object'. """
        self.db.session.delete(object)

    def delete_all_objects(self, ObjectClass, **kwargs):
        """ Delete all objects matching the case sensitive filters in 'kwargs'. """

        # Convert each name/value pair in 'kwargs' into a filter
        query = ObjectClass.query
        for field_name, field_value in kwargs.items():

            # Make sure that ObjectClass has a 'field_name' property
            field = getattr(ObjectClass, field_name, None)
            if field is None:
                raise KeyError(
                    "SQLAlchemyAdapter.find_first_object(): Class '%s' has no field '%s'." % (ObjectClass, field_name))

            # Add a filter to the query
            query = query.filter(field.in_((field_value,)))

        # Execute delete
        # query filter by in_ do not support none args, use synchronize_session=False instead
        query.delete(synchronize_session=False)

    def commit(self):
        self.db.session.commit()