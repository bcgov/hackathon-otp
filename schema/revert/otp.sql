-- Revert everify:otp from pg

BEGIN;

DROP TABLE everify.otp;

COMMIT;
