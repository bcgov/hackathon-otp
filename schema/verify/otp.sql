-- Verify everify:otp on pg

BEGIN;

SELECT email_id, otp, created_at
FROM everify.otp
WHERE FALSE;

ROLLBACK;
