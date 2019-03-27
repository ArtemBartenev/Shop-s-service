"""
This module contains schemas to validate arguments and responses.
"""


company_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "definitions": {
        "kwargs": {
            "type": "object",
            "properties": {
                "company_name": {"type": "string", "minLength": 3, "maxLength": 15},
                "company_email": {"type": "string", "format": "email"},
                "address": {"type": "string"},
                "tel_number": {"type": "string"}
            },
            "required": ["company_name", "address", "company_email", "tel_number"]
        },
    },
    "type": "object",
    "properties": {
        "kwargs": {"$ref": "#/definitions/kwargs"}
    }

}

employee_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "definitions": {
        "kwargs": {
            "type": "object",
            "properties": {
                "first_name": {"type": "string", "minLength": 2},
                "last_name": {"type": "string", "minLength": 2},
                "employee_position": {"type": "string", "minLength": 3},
                "company_name": {"type": "string", "minLength": 3},
                "employee_email": {"type": "string", "format": "email"}
            },
            "required": ["first_name", "last_name", "employee_position", "company_name", "employee_email"]
        },
    },
    "type": "object",
    "properties": {
        "kwargs": {"$ref": "#/definitions/kwargs"}
    }

}

good_adding_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "definitions": {
        "kwargs": {
            "type": "object",
            "properties": {
                "good_name": {"type": "string", "minLength": 3},
                "company_name": {"type": "string", "minLength": 3},
                "good_desc": {"type": "string"}
            },
            "required": ["good_name", "company_name", ]
        },

    },
    "type": "object",
    "properties": {
        "kwargs": {"$ref": "#/definitions/kwargs"}
    }
}

appoint_employee_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "definitions": {
        "kwargs": {
            "type": "object",
            "properties": {
                "employee_first_name": {"type": "string", "minLength": 2},
                "employee_last_name": {"type": "string", "minLength": 2},
                "company_name": {"type": "string", "minLength": 3},
                "good_name": {"type": "string", "minLength": 3}
            },
            "required": ["employee_first_name", "employee_last_name", "company_name", "good_name"]
        }
    },
    "type": "object",
    "properties": {
        "kwargs": {"$ref": "#/definitions/kwargs"}
    }
}
