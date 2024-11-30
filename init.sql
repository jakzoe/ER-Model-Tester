CREATE DATABASE codenight;
CREATE TABLE student
(
studentennummer int PRIMARY KEY,
telefonnummer VARCHAR(50) ,
beraternummer int 
);
CREATE TABLE berater
(
beraternummer int PRIMARY KEY,
telefonnummer VARCHAR(50) 
);
ALTER TABLE student ADD CONSTRAINT fk_beraternummer FOREIGN KEY (beraternummer) REFERENCES berater(beraternummer);