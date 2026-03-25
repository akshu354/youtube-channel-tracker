CREATE TABLE pw_stats (
   video_id varchar(20) NOT NULL,
   title text,
   published_Date date DEFAULT NULL,
   views int DEFAULT NULL,
   likes int DEFAULT NULL,
   duration varchar(20) DEFAULT NULL,
   PRIMARY KEY (video_id)
 ) 