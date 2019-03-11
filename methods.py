# -*- coding: utf-8 -*-
"""Module for working with shop's showcase.

"""
import asyncio
import aiohttp
import psycopg2
from jsonschema import validate
from jsonschema import ValidationError
from service_exceptions import ServiceExecuteError, ServiceValidationError, ServiceConnectionError
from schemas import company_schema, employee_schema, good_adding_schema, appoint_employee_schema
from showcase_db import *


class ShowcaseService:
    """
    Class for interact with shop
    """
    def __init__(self, url: str):
        self._url = url
        self._loop = asyncio.get_event_loop()
        self._registered_http_coros = []
        self._registered_sql_requests = []


    def add_company(self, company_name, address, company_email, tel_number):
        """
        Method for adding new company to shop.
        """
        params = {
            "method": "add_company",
            "kwargs": {
                "company_name": company_name,
                "address": address,
                "tel_number": tel_number,
                "company_email": company_email
            }
        }

        if self._pre_request_validation(params, company_schema):
            self._registered_http_coros.append((params, company_schema))

    def add_employee(self, first_name, last_name, emp_position, company_name, employee_email):
        """
        Method for adding employee of company which already existing in our shop.
        """
        params = {
            "method": "add_employee",
            "kwargs": {
                "first_name": first_name,
                "last_name": last_name,
                "employee_position": emp_position,
                "company_name": company_name,
                "employee_email": employee_email
            }
        }
        if self._pre_request_validation(params, employee_schema):
            self._registered_http_coros.append((params, employee_schema))

    def add_good(self, good_name, good_desc, company_name):
        """
        Method for adding good of company which already existing in our shop.
        """
        params = {
            "method": "add_good",
            "kwargs": {
                "good_name": good_name,
                "company_name": company_name,
                "good_desc": good_desc
            }
        }
        if self._pre_request_validation(params, good_adding_schema):
            self._registered_http_coros.append((params, good_adding_schema))

    def appoint_employee(self, employee_first_name, employee_last_name, company_name, good_name):
        """
        Method for appoint responsible employee for the good.
        """
        params = {
            "method": "appoint_employee",
            "kwargs": {
                "employee_first_name": employee_first_name,
                "employee_last_name": employee_last_name,
                "company_name": company_name,
                "good_name": good_name
            }
        }
        if self._pre_request_validation(params, appoint_employee_schema):
            self._registered_http_coros.append((params, appoint_employee_schema))

    def _pre_request_validation(self, params, schema):
        try:
            validate(params, schema)
        except ValidationError as error:
            raise ServiceValidationError(
                f"Wrong argument(s) in {params['method']} method. {error.message}. Check your arguments => {params}")
        else:
            return True

    def _response_validation(self, schema, resp_dict):
        json = resp_dict.get("json")
        if json:
            try:
                validate(json, schema)
            except ValidationError as error:
                raise ServiceValidationError(
                    f"Received wrong response from server. {error.message}. Check your arguments => {params}")
            else:
                return True

    async def _post_coroutine(self, session, schema, params):
        try:
            response = await session.post(self._url, json=params)
        except aiohttp.ClientConnectionError:
            raise ServiceConnectionError
        else:
            resp_dict = await response.json()
            if self._response_validation(schema, resp_dict):
                self._prepare_sql_requesl(params)
                response.close()
                return resp_dict

    async def _session(self):
        async with aiohttp.ClientSession() as session:
            http_coroutines = []
            for params, schema in self._registered_http_coros:
                http_coroutines.append(self._post_coroutine(session, schema=schema, params=params))
            await asyncio.gather(*http_coroutines)
            self._database_requests()

    def _database_requests(self):
        conn = psycopg2.connect(dsn)
        self._run_sql_request(conn)
        conn.commit()
        conn.close()

    def _prepare_sql_requesl(self, params):
        method = params["method"]
        kwargs = params["kwargs"]
        if method == "add_company":
            self._registered_sql_requests.append((add_company_to_db, kwargs))
        if method == "add_employee":
            self._registered_sql_requests.append((add_employee_to_db, kwargs))
        if method == "add_good":
            self._registered_sql_requests.append((add_good_to_db, kwargs))
        if method == "appoint_employee":
            self._registered_sql_requests.append((appoint_employee_to_db, kwargs))

    def _run_sql_request(self, conn):
        for db_request, kwargs in self._registered_sql_requests:
            cursor = conn.cursor()
            cursor.execute(f'SET search_path TO {CONN_PARAMS["schema"]}')
            db_request(cursor, kwargs)

    def execute(self):
        """
        Main method which execute all planed adding to shop.

        If you call execute() without calling methods "add_company",
        "add_good" e.g. before, it will raise ServiceExecuteError.
        """
        if not self._registered_http_coros:
            raise ServiceExecuteError
        else:
            http_loop = asyncio.get_event_loop()
            http_loop.run_until_complete(self._session())
            http_loop.close()

