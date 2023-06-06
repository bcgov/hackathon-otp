-- Revert everify:verified_email from pg

BEGIN;

DROP TABLE everify.verified_email;

COMMIT;
