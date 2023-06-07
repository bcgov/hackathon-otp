-- Deploy everify:verified_email to pg
-- requires: appschema

BEGIN;

SET client_min_messages = 'warning';

CREATE TABLE everify.verified_email (
    id                  INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    auth_provider_uuid  TEXT NOT NULL,
    email_address       TEXT NOT NULL,
    verified_at         TIMESTAMPTZ
);

COMMIT;
