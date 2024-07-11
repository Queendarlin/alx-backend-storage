-- Stored procedure to add a bonus correction
DELIMITER //

CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    DECLARE project_id INT;

    -- Check if project exists, if not, create it
    SELECT id INTO project_id FROM projects WHERE name = project_name;
    
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Insert the correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
    
    -- Update average_score for the user
    UPDATE users
    SET average_score = (SELECT AVG(score) FROM corrections WHERE user_id = user_id)
    WHERE id = user_id;
    
END //

DELIMITER ;
