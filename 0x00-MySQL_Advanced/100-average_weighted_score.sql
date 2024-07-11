-- Create stored procedure to compute average weighted score
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE avg_score FLOAT;
    
    -- Calculate total score and total weight
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    -- Calculate average weighted score
    IF total_weight > 0 THEN
        SET avg_score = total_score / total_weight;
    ELSE
        SET avg_score = 0;
    END IF;
    
    -- Update the users table with the computed average score
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
    
    -- Select the updated user
    SELECT * FROM users WHERE id = user_id;
    
END //

DELIMITER ;
