-- Deploy everify:otp to pg
-- requires: appschema

BEGIN;

SET client_min_messages = 'warning';

CREATE TABLE everify.otp (
    id          INTEGER GENERATED ALWAYS AS IDENTITY,
    email_id    INTEGER,
    otp         TEXT,
    created_at  TIMESTAMPTZ NOT NULL    DEFAULT NOW(),
    PRIMARY KEY(id),
    CONSTRAINT fk_email
        FOREIGN KEY(email_id)
            REFERENCES everify.verified_email(id)
);

COMMIT;
