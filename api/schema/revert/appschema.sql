-- Revert everify:appschema from pg

BEGIN;

DROP SCHEMA everify;

COMMIT;
