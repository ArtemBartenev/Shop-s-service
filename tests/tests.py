import unittest
import methods
import aiohttp
import asyncio
import psycopg2
from schemas import company_schema
from service_exceptions import ServiceValidationError, ServiceExecuteError
from showcase_db import dsn, add_company_to_db, CONN_PARAMS



class ValidationTest(unittest.TestCase):

    def setUp(self):
        self.url = "test_url"
        self.service = methods.ShowcaseService(self.url)

        self.schema = company_schema

    def test_successful_validation(self):
        self.params = {
            "method": "add_company",
            "kwargs": {
                "company_name": "Romashka",
                "address": "Moscow",
                "company_email": "enterprise@romashka.com",
                "tel_number": "555-55-55"
            }
        }
        self.assertTrue(self.service._pre_request_validation(self.params, self.schema))

    def test_unsuccessful_validation(self):
        self.params = {
            "method": "add_company",
            "kwargs": {
                "company_name": ["Romashka"],
                "address": "Moscow",
                "company_email": 0.0,
                "tel_number": "555-55-55"
            }
        }
        self.assertRaises(ServiceValidationError, self.service._pre_request_validation, self.params, self.schema)

    def tearDown(self):
        self.service = None


class ServiceExcecuteTest(unittest.TestCase):
    def setUp(self):
        self.url = "test_url"
        self.service = methods.ShowcaseService(self.url)

    def test_execute(self):
        self.assertRaises(ServiceExecuteError, self.service.execute)

    def tearDown(self):
        self.service = None


class ResponseValidation(unittest.TestCase):
    def setUp(self):
        self.url = "http://httpbin.org/post"
        self.params = {
            "method": "add_company",
            "kwargs": {
                "company_name": "Romashka",
                "address": "Moscow",
                "company_email": "enterprise@romashka.com",
                "tel_number": "555-55-55"
            }
        }

        self.service = methods.ShowcaseService(self.url)
        self.schema = company_schema
        self.event_loop = asyncio.get_event_loop()

    def test_response_validation(self):
        task = self.event_loop.create_task(self.coroutine())
        resp_dict = self.event_loop.run_until_complete(task)
        self.assertEqual(resp_dict['json'], self.params)
        self.event_loop.close()

    async def coroutine(self):
        async with aiohttp.ClientSession() as session:
            resp_dict = await self.service._post_coroutine(session, self.schema, self.params)
            return resp_dict

    def tearDown(self):
        self.service = None
        self.schema = None
        self.params = None
        self.event_loop = None

@unittest.skip("Database not initialised")
class DataBaseRequestTest(unittest.TestCase):
    def setUp(self):
        self.kwargs = {
            "company_name": "Romashka",
            "address": "Moscow",
            "company_email": "enterprise@romashka.com",
            "tel_number": "555-55-55"
        }
        self.conn = psycopg2.connect(dsn=dsn)
        self.cursor = self.conn.cursor()

    def test_db_request(self):
        self.cursor.execute(f'SET search_path TO {CONN_PARAMS["schema"]}')
        add_company_to_db(self.cursor, self.kwargs)
        select_cursor = self.conn.cursor()
        select_cursor.execute("SELECT company_name, address, tel_number, company_email FROM company WHERE "
                            "company_name = %(company_name)s", (self.kwargs))
        result = select_cursor.fetchall()[0]
        self.assertEqual(list(self.kwargs.values()).sort(), list(result).sort())


    def tearDown(self):
        self.conn.close()