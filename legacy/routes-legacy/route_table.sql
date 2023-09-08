-- noinspection SqlNoDataSourceInspectionForFile

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE routes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    flightId VARCHAR UNIQUE NOT NULL,
    sourceAirportCode VARCHAR NOT NULL,
    sourceCountry VARCHAR NOT NULL,
    destinyAirportCode VARCHAR NOT NULL,
    destinyCountry VARCHAR NOT NULL,
    bagCost INT NOT NULL,
    plannedStartDate TIMESTAMP NOT NULL,
    plannedEndDate TIMESTAMP NOT NULL,
    createdAt TIMESTAMP NOT NULL,
    updatedAt TIMESTAMP NOT NULL
);