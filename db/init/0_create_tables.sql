-- DROP TABLE IF EXISTS "user";
-- DELETE FROM "user";
-- 
-- NOTE Table名は""でくくらなければ小文字化されるので,小文字で統一
-- idの長さ=ユーザIDの仕様で決められた制限文字数
-- nameの長さ=ユーザ名の仕様で決められた制限文字数
CREATE TABLE IF NOT EXISTS "user" (
    id VARCHAR(32) NOT NULL,
    name VARCHAR(32) NOT NULL,
    PRIMARY KEY (id)
);