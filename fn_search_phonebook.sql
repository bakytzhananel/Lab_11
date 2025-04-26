CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, first_name TEXT, phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    WHERE first_name ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;
