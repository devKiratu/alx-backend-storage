-- This script creates a stored procedure ComputeAverageWeightedScoreForUsers that
-- computes and store the average weighted score for all students. 
-- Requirements:
--  Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

-- clear existing procedure
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  DECLARE done INT DEFAULT FALSE;
  DECLARE user_id INT;
  DECLARE user_cursor CURSOR FOR SELECT id FROM users;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  OPEN user_cursor;

  read_loop: LOOP
    FETCH user_cursor INTO user_id;
    IF done THEN
      LEAVE read_loop;
    END IF;

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

  END LOOP;

  CLOSE user_cursor;

END;
$$
DELIMITER ;
