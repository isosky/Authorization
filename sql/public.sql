/*
Navicat PGSQL Data Transfer

Source Server         : localhost
Source Server Version : 90505
Source Host           : localhost:5432
Source Database       : authorization
Source Schema         : public

Target Server Type    : PGSQL
Target Server Version : 90505
File Encoding         : 65001

Date: 2017-09-06 18:40:02
*/


-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_group";
CREATE TABLE "public"."auth_group" (
"g_id" int4 NOT NULL,
"g_f_id" int4,
"group_name" varchar(30) COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
INSERT INTO "public"."auth_group" VALUES ('0', null, 'asialantao');
INSERT INTO "public"."auth_group" VALUES ('1', '0', 'A');
INSERT INTO "public"."auth_group" VALUES ('2', '0', 'B');
INSERT INTO "public"."auth_group" VALUES ('3', '1', 'A_A');
INSERT INTO "public"."auth_group" VALUES ('4', '3', 'A_A_A');
INSERT INTO "public"."auth_group" VALUES ('5', '1', 'A_B');

-- ----------------------------
-- Table structure for auth_group_per
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_group_per";
CREATE TABLE "public"."auth_group_per" (
"g_id" int4,
"p_id" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of auth_group_per
-- ----------------------------

-- ----------------------------
-- Table structure for auth_per
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_per";
CREATE TABLE "public"."auth_per" (
"p_id" int4 NOT NULL,
"permit_name" varchar(40) COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of auth_per
-- ----------------------------
INSERT INTO "public"."auth_per" VALUES ('1', '权限1');
INSERT INTO "public"."auth_per" VALUES ('2', '权限2');
INSERT INTO "public"."auth_per" VALUES ('3', '权限3');

-- ----------------------------
-- Table structure for auth_role_group
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_role_group";
CREATE TABLE "public"."auth_role_group" (
"r_id" int4 NOT NULL,
"g_id" int4,
"role_name" varchar(30) COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of auth_role_group
-- ----------------------------
INSERT INTO "public"."auth_role_group" VALUES ('1', '1', '部门1的实习生');
INSERT INTO "public"."auth_role_group" VALUES ('2', '1', '部门1的正式员工');
INSERT INTO "public"."auth_role_group" VALUES ('3', '1', '部门1的管理');

-- ----------------------------
-- Table structure for auth_role_per
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_role_per";
CREATE TABLE "public"."auth_role_per" (
"r_id" int4,
"p_id" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of auth_role_per
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_user";
CREATE TABLE "public"."auth_user" (
"user_id" int4 NOT NULL,
"g_id" int4,
"r_id" int4,
"user_name" varchar(20) COLLATE "default",
"last_login" timestamp(6),
"isroot" bool,
"login_name" varchar(30) COLLATE "default",
"pwd" varchar(30) COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO "public"."auth_user" VALUES ('1', null, null, 'admin', null, null, null, null);
INSERT INTO "public"."auth_user" VALUES ('2', '1', '3', '李晨放', null, 'f', 'lcf', 'None');

-- ----------------------------
-- Table structure for auth_user_per
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_user_per";
CREATE TABLE "public"."auth_user_per" (
"user_id" int4,
"p_id" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of auth_user_per
-- ----------------------------

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table auth_group
-- ----------------------------
ALTER TABLE "public"."auth_group" ADD PRIMARY KEY ("g_id");

-- ----------------------------
-- Primary Key structure for table auth_per
-- ----------------------------
ALTER TABLE "public"."auth_per" ADD PRIMARY KEY ("p_id");

-- ----------------------------
-- Primary Key structure for table auth_role_group
-- ----------------------------
ALTER TABLE "public"."auth_role_group" ADD PRIMARY KEY ("r_id");

-- ----------------------------
-- Primary Key structure for table auth_user
-- ----------------------------
ALTER TABLE "public"."auth_user" ADD PRIMARY KEY ("user_id");

-- ----------------------------
-- Foreign Key structure for table "public"."auth_group_per"
-- ----------------------------
ALTER TABLE "public"."auth_group_per" ADD FOREIGN KEY ("g_id") REFERENCES "public"."auth_group" ("g_id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."auth_group_per" ADD FOREIGN KEY ("p_id") REFERENCES "public"."auth_per" ("p_id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."auth_role_group"
-- ----------------------------
ALTER TABLE "public"."auth_role_group" ADD FOREIGN KEY ("g_id") REFERENCES "public"."auth_group" ("g_id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."auth_role_per"
-- ----------------------------
ALTER TABLE "public"."auth_role_per" ADD FOREIGN KEY ("r_id") REFERENCES "public"."auth_role_group" ("r_id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."auth_role_per" ADD FOREIGN KEY ("p_id") REFERENCES "public"."auth_per" ("p_id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."auth_user"
-- ----------------------------
ALTER TABLE "public"."auth_user" ADD FOREIGN KEY ("r_id") REFERENCES "public"."auth_role_group" ("r_id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."auth_user" ADD FOREIGN KEY ("g_id") REFERENCES "public"."auth_group" ("g_id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Key structure for table "public"."auth_user_per"
-- ----------------------------
ALTER TABLE "public"."auth_user_per" ADD FOREIGN KEY ("user_id") REFERENCES "public"."auth_user" ("user_id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."auth_user_per" ADD FOREIGN KEY ("p_id") REFERENCES "public"."auth_per" ("p_id") ON DELETE NO ACTION ON UPDATE NO ACTION;
