-- Deploy everify:verified_email to pg
-- requires: appschema

BEGIN;

SET client_min_messages = 'warning';

CREATE TABLE everify.verified_email (
    id                  INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    auth_provider_uuid  TEXT NOT NULL,
    email_address       TEXT        NOT NULL,
    is_verified         BOOLEAN     NOT NULL    DEFAULT false,
    verified_at         TIMESTAMPTZ NOT NULL    DEFAULT NOW()
);

COMMIT;
