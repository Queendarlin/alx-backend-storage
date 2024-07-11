-- Defines SafeDiv function
-- The function checks if the divisor (b) is zero and returns 0 in that case to avoid division errors

DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT

BEGIN
    DECLARE result FLOAT;

    IF b = 0 THEN
        SET result = 0;
    ELSE
        SET result = a / b;
    END IF;

    RETURN result;
END//

DELIMITER ;
