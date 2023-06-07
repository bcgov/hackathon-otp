-- Deploy everify:otp to pg
-- requires: appschema

BEGIN;

SET client_min_messages = 'warning';

CREATE TABLE everify.otp (
    id          INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    email_id    INTEGER REFERENCES everify.verified_email(id),
    otp         TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMIT;
