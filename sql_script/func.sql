CREATE FUNCTION hamming_distance(simhash1 VARCHAR(64), simhash2 VARCHAR(64)) RETURNS INT
BEGIN
    DECLARE t1 BIGINT UNSIGNED;
    DECLARE t2 BIGINT UNSIGNED;
    DECLARE n BIGINT UNSIGNED;
    DECLARE distance INT DEFAULT 0;
    
    -- 将二进制字符串转换为十进制格式
    SET t1 = CONV(simhash1, 2, 10);
    SET t2 = CONV(simhash2, 2, 10);
    
    -- 计算汉明距离
    SET n = t1 ^ t2;
    SET distance = BIT_COUNT(n);
    
    RETURN distance;
END 



CREATE FUNCTION similarity(simhash1 VARCHAR(64), simhash2 VARCHAR(64)) RETURNS FLOAT
BEGIN
    DECLARE hanming INT;
    DECLARE res FLOAT;
    
    -- 计算汉明距离
    SET hanming = hamming_distance(simhash1, simhash2);
    
    -- 计算相似度
    SET res = 1 - (hanming / LENGTH(simhash1));
    
    RETURN res;
END 



