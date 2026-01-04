-- prisma/rls_setup.sql

-- 1. Enable RLS on the table
ALTER TABLE intuitions ENABLE ROW LEVEL SECURITY;

-- 2. Create the policy
-- Only allow users to see their own records based on 'app.current_user' set in session
CREATE POLICY user_isolation_policy ON intuitions
FOR ALL
USING (userId::text = current_setting('app.current_user'));

-- 3. In the Prisma repository, we must call:
-- SET app.current_user = '...user_id...';
-- Before any query.
