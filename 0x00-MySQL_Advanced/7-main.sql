-- Show users and corrections
SELECT * FROM users;
SELECT * FROM corrections;

SELECT "--";

-- Execute the stored procedure to compute average score for user "Jeanne"
CALL ComputeAverageScoreForUser((SELECT id FROM users WHERE name = "Jeanne"));

SELECT "--";

-- Show updated users table with average scores
SELECT * FROM users;
