SELECT nspname AS name
  FROM pg_namespace
 WHERE nspname NOT IN ('information_schema', 'pg_toast', 'pg_internal', 'pg_catalog')
       AND nspname NOT LIKE 'pg_temp%';

