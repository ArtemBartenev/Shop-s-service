"""
Database connection parameters and functions to request.
"""

import psycopg2
from service_exceptions import ServiceDataBaseError

CONN_PARAMS = {
    "host": "localhost",
    "database": "test",
    "user": "postgres",
    "password": "postgres",
    "schema": "service"
}

dsn = 'dbname={database} user={user} password={password} host={host}'.format(**CONN_PARAMS)


def add_company_to_db(cursor, kwargs):
    """
    Function for adding new company to database.
    """
    try:
        cursor.execute("INSERT INTO company(company_name, address, company_email, tel_number) "
                       "values(%(company_name)s, %(address)s, %(company_email)s, %(tel_number)s)", (kwargs))
    except psycopg2.IntegrityError:
        raise ServiceDataBaseError(f"Company name - {kwargs['company_name']} already registered")
    finally:
        cursor.close()


def add_employee_to_db(cursor, kwargs):
    """
    Function for adding employee to database.
    """
    try:
        cursor.execute(
            "INSERT INTO employee(employee_first_name, employee_last_name, employee_email, employee_position, company_name)"
            "values (%(first_name)s, %(last_name)s, %(employee_email)s, %(employee_position)s, %(company_name)s)",
            (kwargs))
    except psycopg2.IntegrityError:
        raise ServiceDataBaseError(f"Company name - \"{kwargs['company_name']}\" is not registered yet")
    cursor.close()


def add_good_to_db(cursor, kwargs):
    """
    Function for adding good to database.
    """
    cursor.execute("SELECT company_id FROM company WHERE company_name = %(company_name)s", (kwargs))
    company_id = cursor.fetchone()
    if company_id is None:
        raise ServiceDataBaseError(f"Company name - \"{kwargs['company_name']}\" is not registered yet")
    cursor.execute(
        "INSERT INTO good(good_name, good_desc) values (%(good_name)s, %(good_desc)s) RETURNING good_id",
        (kwargs))
    good_id = cursor.fetchone()
    cursor.execute("INSERT INTO good_company (good_id, company_id) values(%s, %s) ", (good_id, company_id))
    cursor.close()


def appoint_employee_to_db(cursor, kwargs):
    """
    Function for appoint employee for the good.
    """
    cursor.execute(
        "SELECT g.good_id FROM good g INNER JOIN good_company gc ON g.good_id = gc.good_id "
        "INNER JOIN company c ON gc.company_id = c.company_id"
        " WHERE c.company_name = %(company_name)s AND g.good_name = %(good_name)s", (kwargs))
    good_id = cursor.fetchone()
    if good_id is None:
        raise ServiceDataBaseError(
            f"Good name \"{kwargs['good_name']}\" is not registered with the company \"{kwargs['company_name']}\". "
            f"Check both names")
    cursor.execute("SELECT employee_id FROM employee e WHERE employee_first_name = %(employee_first_name)s AND "
                   "employee_last_name = %(employee_last_name)s AND company_name = %(company_name)s", (kwargs))

    employee_id = cursor.fetchone()
    if employee_id is None:
        raise ServiceDataBaseError(
            f"There is no employee with that name  \"{kwargs['employee_first_name']} {kwargs['employee_last_name']}\""
            f" in company \"{kwargs['company_name']}\"")
    cursor.execute("INSERT INTO service.good_employee(good_id, employee_id) values(%s, %s)", (good_id, employee_id))
    cursor.close()
