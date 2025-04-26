CREATE OR REPLACE PROCEDURE insert_many_users(
    p_names TEXT[],
    p_phones TEXT[],
    OUT invalid_entries TEXT[]
)
AS $$
DECLARE
    i INT := 1;
    phone_pattern TEXT := '^[0-9+\-() ]{7,20}$';  -- Example validation
BEGIN
    invalid_entries := '{}';

    WHILE i <= array_length(p_names, 1) LOOP
        IF p_phones[i] ~ phone_pattern THEN
            CALL insert_or_update_user(p_names[i], p_phones[i]);
        ELSE
            invalid_entries := array_append(invalid_entries, p_names[i] || ' - ' || p_phones[i]);
        END IF;
        i := i + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
