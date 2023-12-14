-- This script creates a stored procedure ComputeAverageWeightedScoreForUser that
-- computes and store the average weighted score for a student.
-- Requirements:
--  Procedure ComputeAverageScoreForUser is taking 1 input:
--    user_id, a users.id value (you can assume user_id is linked to an existing users)

-- clear existing procedure
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
  SET @weight = (SELECT SUM(p.weight)
  FROM corrections c
  JOIN projects p ON p.id = c.project_id
  WHERE c.user_id = user_id);

  SET @score = (SELECT SUM(p.weight * c.score)
  FROM corrections c
  JOIN projects p ON p.id = c.project_id
  WHERE c.user_id = user_id);

  SET @avg_wts = (@score / @weight);
  
  UPDATE users
  SET users.average_score = @avg_wts
  WHERE users.id = user_id;

END;
$$
DELIMITER ;
