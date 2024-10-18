-- SQL script that creates a stored procedure AddBonus

DROP PROCEDURE IF EXISTS AddBonus;

DELIMITER $$
CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255), 
    IN score INT
)
    BEGIN
        IF (SELECT COUNT(*) FROM projects WHERE name = project_name) = 0
            THEN
                INSERT INTO projects (name) VALUES (project_name);
        END IF;
        SET @projectID = (SELECT id FROM projects WHERE name = project_name);
        INSERT INTO corrections(user_id, project_id, score)
            VALUES (user_id, @projectID, score);
    END;
$$
DELIMITER ;
