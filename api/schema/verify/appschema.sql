-- Verify everify:appschema on pg

BEGIN;

SELECT pg_catalog.has_schema_privilege('everify', 'usage');

ROLLBACK;
