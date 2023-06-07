-- Verify everify:verified_email on pg

BEGIN;

SELECT auth_provider_uuid, email_address, is_verified, verified_at
FROM everify.verified_email
WHERE FALSE;

ROLLBACK;
