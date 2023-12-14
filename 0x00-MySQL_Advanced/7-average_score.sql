-- This script creates a stored procedure ComputeAverageScoreForUser that computes 
--  and store the average score for a student. Note: An average score can be a decimal
-- Requirements:
--  Procedure ComputeAverageScoreForUser is taking 1 input:
--    - user_id, a users.id value (you can assume user_id is linked to an existing users)

-- clear previous procedure
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
  SET @avg_score = (SELECT AVG(score) FROM corrections WHERE corrections.user_id = user_id);
  UPDATE users SET users.average_score = @avg_score WHERE users.id = user_id;
END;
$$
DELIMITER ;
