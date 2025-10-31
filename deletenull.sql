UPDATE batting_stats 
SET H = 3, OE = 0 
WHERE PlayerNumber = 401 
AND TeamNumber = 534 
AND GameNumber = 15;

DELETE FROM batting_stats 
WHERE PA = 0 
AND R = 0 
AND H = 0 
AND `2B` = 0 
AND `3B` = 0 
AND HR = 0 
AND RBI = 0 
AND SF = 0;