CREATE OR REPLACE FUNCTION get_users_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, first_name TEXT, phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    ORDER BY id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
