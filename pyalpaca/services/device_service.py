#!/usr/bin/env python
#
# Copyright 2013 Rodrigo Ancavil del Pino
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# -*- coding: utf-8 -*-

import tornado.ioloop
from tornado.httputil import parse_body_arguments

import pyrestful.rest
import json

from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete

import sys
from .config import getDriverInstance

from .httpresponses import HttpSuccessResponse, HttpErrorResponse


class DeviceService(pyrestful.rest.RestHandler):
    def get_resource(self, device_type, device_number, resource, *args):
        print("Trying to get resource: " + resource + " for device type: " + device_type)
        driver = getDriverInstance(device_type, device_number)
        response = None

        try:
            if (driver is None):
                raise ValueError("Driver not loaded. Check your server configuration.")
                
            # Dynamically call the method/property if it exists 
            attr = getattr(driver, resource)
            if callable(attr):
                # might be a class instance method
                print("Arguments passed: " + str(args))
                value = attr(*args)
                print("Value got: "+str(value))
            else:
                # might be a property
                print(f"Value is a property: {attr}")
                value = attr

            response = {
                "ClientTransactionID": 0,
                "ServerTransactionID": 0,
                "ErrorNumber": 0,
                "ErrorMessage": ""
            }

            if not (value is None):
                print("Setting value in response = "+str(value))
                response["Value"] = value

        except Exception as exc:
            response = {
                "Value": str(exc)
            }
            self.set_status(500, str(exc))
        finally:
            self.write(response)
            self.finish()

    def set_resource(self, device_type, device_number, resource, resource_value):
        driver = getDriverInstance(device_type, device_number)
        print("Trying to set resource: " + resource + " with value " + str(resource_value) + " for device type: " + device_type)
        try:
            if (driver is None):
                raise ValueError("Driver not loaded. Check your server configuration.")

            # Dynamically call the method/property if it exists
            setattr(driver, resource, resource_value)

            response = {
                "ClientTransactionID": 0,
                "ServerTransactionID": 0,
                "ErrorNumber": 0,
                "ErrorMessage": ""
            }
        except Exception as exc:
            response = {
                "Value": str(exc)
            }
            self.set_status(500, str(exc))

        self.write(response)
        self.finish()

    def get_query_argument_for_get_request(self, argument):
        return self.request.query_arguments[argument][0].decode()

    def get_string_values_from_put_request(self, *arguments):
        # read www/x-www-form-urlencoded parameters
        string_values = []
        if self.request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
            values = {}
            files = {}
            parse_body_arguments('application/x-www-form-urlencoded', self.request.body, values, files)
            return [values[arg][0].decode() for arg in arguments]
        else:
            raise ValueError

    def set_one_boolean_resource(self, device_type, device_number, ascom_attribute_name, driver_attribute_name):
        try:
            value_str = self.get_string_values_from_put_request(ascom_attribute_name)
            self.set_resource(device_type, device_number, driver_attribute_name, value_str[0] == 'True')
        except ValueError:
            self.set_status(400, "Value error")

    def set_one_integer_resource(self, device_type, device_number, ascom_attribute_name, driver_attribute_name):
        try:
            value_str = self.get_string_values_from_put_request(ascom_attribute_name)
            self.set_resource(device_type, device_number, driver_attribute_name, int(value_str[0]))
        except ValueError:
            self.set_status(400, "Value error")

    def set_one_float_resource(self, device_type, device_number, ascom_attribute_name, driver_attribute_name):
        try:
            value_str = self.get_string_values_from_put_request(ascom_attribute_name)
            self.set_resource(device_type, device_number, driver_attribute_name, float(value_str[0]))
        except ValueError:
            self.set_status(400, "Value error")

    def standard_response_for_put(self, device_type, device_number, foo):
        try:
            driver = getDriverInstance(device_type, device_number)
            if driver is None:
                raise ValueError("Driver not loaded. Check your server configuration.")

            foo(driver)

            response = {
                "ClientTransactionID": 0,
                "ServerTransactionID": 0,
                "ErrorNumber": 0,
                "ErrorMessage": ""
            }
        except Exception as exc:
            response = {
                "Value": str(exc)
            }
            self.set_status(500, str(exc))

        self.write(response)
        self.finish()

    @get(_path="/api/v1/{device_type}/{device_number}/name", _types=[str, int, str], _produces=mediatypes.APPLICATION_JSON)
    def get_name(self, device_type, device_number):
        self.get_resource(device_type, device_number, "name")

    @get(_path="/api/v1/{device_type}/{device_number}/description", _types=[str, int, str],
         _produces=mediatypes.APPLICATION_JSON)
    def get_description(self, device_type, device_number):
        self.get_resource(device_type, device_number, "description")

    @get(_path="/api/v1/{device_type}/{device_number}/driverinfo", _types=[str, int, str],
         _produces=mediatypes.APPLICATION_JSON)
    def get_driver_info(self, device_type, device_number):
        self.get_resource(device_type, device_number, "driver_info")    \

    @get(_path="/api/v1/{device_type}/{device_number}/driverversion", _types=[str, int, str],
         _produces=mediatypes.APPLICATION_JSON)
    def get_driver_version(self, device_type, device_number):
        self.get_resource(device_type, device_number, "driver_version")

    @get(_path="/api/v1/{device_type}/{device_number}/interfaceversion", _types=[str, int, str], _produces=mediatypes.APPLICATION_JSON)
    def get_interface_version(self, device_type, device_number):
        self.get_resource(device_type, device_number, "interface_version")

    @get(_path="/api/v1/{device_type}/{device_number}/supportedactions", _types=[str, int, str], _produces=mediatypes.APPLICATION_JSON)
    def get_supported_actions(self, device_type, device_number):
        self.get_resource(device_type, device_number, "supported_actions")

    @get(_path="/api/v1/{device_type}/{device_number}/connected", _types=[str, int, str], _produces=mediatypes.APPLICATION_JSON)
    def get_connected(self, device_type, device_number):
        self.get_resource(device_type, device_number, "connected")

    @put(_path="/api/v1/{device_type}/{device_number}/connected", _types=[str, int, str], _produces=mediatypes.APPLICATION_JSON)
    def set_connected(self, device_type, device_number):
        self.set_one_boolean_resource(device_type, device_number, "Connected", "connected")

    # TODO PUT !
