CREATE TABLE service.company (
	company_id serial NOT NULL PRIMARY KEY,
	company_name varchar(128) NOT NULL UNIQUE,
	address varchar(128) NOT NULL,
	tel_number varchar(32) NULL,
	company_email varchar(64) NOT NULL,
);


CREATE TABLE service.employee (
	employee_id serial NOT NULL PRIMARY KEY,
	employee_first_name varchar(128) NOT NULL,
	employee_last_name varchar(128) NOT NULL,
	employee_position varchar(64) NOT NULL,
	company_name varchar(128) NOT NULL REFERENCES company(company_name) ON DELETE CASCADE ,
	employee_email varchar(64) NOT NULL,
);

CREATE TABLE service.good (
	good_id serial NOT NULL PRIMARY KEY,
	good_name varchar(128) NOT NULL,
	good_desc varchar(128) NOT NULL,
);


CREATE TABLE service.good_company (
	id serial NOT NULL PRIMARY KEY,
	good_id integer NOT NULL REFERENCES good(good_id) ON DELETE CASCADE,
	company_id integer NOT NULL REFERENCES company(company_id) ON DELETE CASCADE,
);


CREATE TABLE service.good_employee (
	id serial NOT NULL PRIMARY KEY,
	good_id integer NOT NULL REFERENCES good(good_id) ON DELETE CASCADE,
	employee_id integer NOT NULL REFERENCES employee(employee_id) ON DELETE CASCADE,
);
