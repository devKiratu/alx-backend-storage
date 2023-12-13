-- This script creates a trigger that resets the attribute valid_email only when the email has been changed.

-- clear previous trigger
DROP TRIGGER IF EXISTS valid_email_check;

DELIMITER $$
CREATE TRIGGER valid_email_check
BEFORE UPDATE
ON users FOR EACH ROW
BEGIN
        IF NEW.email <> OLD.email THEN
                SET NEW.valid_email = NOT NEW.valid_email;
        END IF;
END;
$$
DELIMITER ;
