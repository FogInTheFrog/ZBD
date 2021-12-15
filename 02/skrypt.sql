DROP TABLE edge;
DROP TABLE address;
DROP TABLE entity;
DROP TABLE intermediary;
DROP TABLE officer;

DROP TABLE country;
DROP TABLE jurisdiction;

CREATE TABLE edge (
    start_id INTEGER,
    type VARCHAR(20),
    end_id INTEGER,
    link VARCHAR(50),
    start_date VARCHAR(15),
    end_date VARCHAR(15),
    sourceID VARCHAR(15),
    valid_until VARCHAR(50)
);

CREATE TABLE address (
    node_id INTEGER PRIMARY KEY,
    name VARCHAR(1),
    address TEXT,
    country_codes VARCHAR(3),
    sourceID VARCHAR(15),
    valid_until VARCHAR(50),
    note VARCHAR(1)
);

CREATE TABLE entity (
    node_id INTEGER PRIMARY KEY,
    name VARCHAR(150),
    jurisdiction_code VARCHAR(5),
    country_codes VARCHAR(5),
    incorporation_date VARCHAR(15),
    inactivation_date VARCHAR(15),
    struck_off_date VARCHAR(15),
    closed_date VARCHAR(5),
    ibcRUC VARCHAR(20),
    status VARCHAR(35),
    company_type VARCHAR(1),
    service_provider VARCHAR(15),
    sourceID VARCHAR(15),
    valid_until VARCHAR(50),
    note TEXT
);

CREATE TABLE intermediary (
    node_id INTEGER PRIMARY KEY,
    name VARCHAR(90),
    country_codes VARCHAR(10),
    status VARCHAR(35),
    sourceID VARCHAR(15),
    valid_until VARCHAR(50),
    note TEXT
);

CREATE TABLE officer (
    node_id INTEGER PRIMARY KEY,
    name TEXT,
    country_codes VARCHAR(10),
    sourceID VARCHAR(15),
    valid_until VARCHAR(50),
    note TEXT
);

CREATE TABLE jurisdiction (
    code VARCHAR(10) PRIMARY KEY,
    description VARCHAR(50)
);

CREATE TABLE country (
    code VARCHAR(10) PRIMARY KEY,
    description VARCHAR(50)
);

\copy edge FROM 'panama_papers.edges.csv' with (format csv,header true, delimiter ',');

CREATE TABLE temp_address (
    node_id INTEGER PRIMARY KEY,
    name VARCHAR(1),
    address VARCHAR(750),
    country_codes VARCHAR(3),
    countries VARCHAR(50),
    sourceID VARCHAR(15),
    valid_until VARCHAR(50),
    note VARCHAR(1)
);

CREATE TABLE temp_entity (
    node_id INTEGER PRIMARY KEY,
    name VARCHAR(150),
    jurisdiction_code VARCHAR(5),
    jurisdiction_description VARCHAR(25),
    country_codes VARCHAR(5),
    countries VARCHAR(50),
    incorporation_date VARCHAR(15),
    inactivation_date VARCHAR(15),
    struck_off_date VARCHAR(15),
    closed_date VARCHAR(5),
    ibcRUC VARCHAR(20),
    status VARCHAR(35),
    company_type VARCHAR(1),
    service_provider VARCHAR(15),
    sourceID VARCHAR(15),
    valid_until VARCHAR(50),
    note TEXT
);

CREATE TABLE temp_intermediary (
    node_id INTEGER PRIMARY KEY,
    name VARCHAR(90),
    country_codes VARCHAR(10),
    countries VARCHAR(50),
    status VARCHAR(35),
    sourceID VARCHAR(15),
    valid_until VARCHAR(50),
    note TEXT
);

CREATE TABLE temp_officer (
    node_id INTEGER PRIMARY KEY,
    name TEXT,
    country_codes VARCHAR(10),
    countries VARCHAR(50),
    sourceID VARCHAR(15),
    valid_until VARCHAR(50),
    note TEXT
);

\copy temp_address FROM 'panama_papers.nodes.address.csv' with (format csv, header true, delimiter ',');

INSERT INTO address (node_id, name, address, country_codes, sourceID, valid_until, note)
SELECT node_id, name, address, country_codes, sourceID, valid_until, note FROM temp_address;

INSERT INTO country (code, description)
SELECT country_codes, countries FROM temp_address
ON CONFLICT DO NOTHING;

DROP TABLE temp_address;



\copy temp_officer FROM 'panama_papers.nodes.officer.csv' with (format csv, header true, delimiter ',');

INSERT INTO officer (node_id, name, country_codes, sourceID, valid_until, note)
SELECT node_id, name, country_codes, sourceID, valid_until, note FROM temp_officer;

INSERT INTO country (code, description)
SELECT country_codes, countries FROM temp_officer
ON CONFLICT DO NOTHING;

DROP TABLE temp_officer;



\copy temp_intermediary FROM 'panama_papers.nodes.intermediary.csv' with (format csv, header true, delimiter ',');

INSERT INTO intermediary (node_id, name, country_codes, status, sourceID, valid_until, note)
SELECT node_id, name, country_codes, status, sourceID, valid_until, note FROM temp_intermediary;

INSERT INTO country (code, description)
SELECT country_codes, countries FROM temp_intermediary
ON CONFLICT DO NOTHING;

DROP TABLE temp_intermediary;



\copy temp_entity FROM 'panama_papers.nodes.entity.csv' with (format csv, header true, delimiter ',');

INSERT INTO entity (node_id, name, jurisdiction_code, country_codes, incorporation_date,
inactivation_date, struck_off_date, closed_date, ibcRUC, status, company_type, service_provider,
sourceID, valid_until, note)

SELECT node_id, name, jurisdiction_code, country_codes, incorporation_date,
inactivation_date, struck_off_date, closed_date, ibcRUC, status, company_type, service_provider,
sourceID, valid_until, note FROM temp_entity;

INSERT INTO country (code, description)
SELECT country_codes, countries FROM temp_entity
ON CONFLICT DO NOTHING;

INSERT INTO jurisdiction (code, description)
SELECT jurisdiction_code, jurisdiction_description FROM temp_entity
ON CONFLICT DO NOTHING;

DROP TABLE temp_entity;

