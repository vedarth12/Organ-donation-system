CREATE DATABASE FINAL_DBMS;
USE FINAL_DBMS; 

CREATE TABLE login(
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL
);

INSERT INTO login VALUES ('admin','admin');

CREATE TABLE Organization(
  Organization_ID int NOT NULL auto_increment,
  Organization_name varchar(20) NOT NULL,
  Location varchar(20),
  Phone_no char(10),
  Government_approved int, # 0 or 1
  PRIMARY KEY(Organization_ID)
);

CREATE TABLE Doctor(
  Doctor_ID int NOT NULL auto_increment,
  Doctor_Name varchar(20) NOT NULL unique,
  Gender varchar(6) not null check(Gender in ('Male', 'Female', 'Other')),
  Phone_no char(10),
  Department_Name varchar(20) NOT NULL,
  Organization_ID int NOT NULL,
  FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) on delete cascade,
  PRIMARY KEY(Doctor_ID)
);

CREATE TABLE Organization_head(
  Organization_ID int NOT NULL,
  Name varchar(20) NOT NULL,
  Date_of_joining date NOT NULL,
  FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) on delete cascade
);

CREATE TABLE Patient(
	Patient_ID int primary key NOT NULL auto_increment ,
    Name varchar(20) NOT NULL,
    Date_of_Birth date NOT NULL,
    Gender varchar(6) not null check(Gender in ('Male', 'Female', 'Other')),
    Phone_no char(10),
    Address varchar(50),
    organ_req varchar(20) NOT NULL check(organ_req in ('lungs', 'pancreas', 'kidney', 'liver')),
    reason_of_procurement varchar(20),
    Doctor_Name varchar(20) NOT NULL,
    FOREIGN KEY(Doctor_Name) REFERENCES Doctor(Doctor_Name) on delete cascade
);

CREATE TABLE Patient_Medical_History(
    Patient_ID int,
	Diabetes varchar(5) not null check(Diabetes in ('Yes','No')),
    High_Blood_Pressure varchar(5) not null check(High_Blood_Pressure in ('Yes','No')),
    High_Cholesterol varchar(5) not null check(High_Cholesterol in ('Yes','No')),
    Asthma varchar(5) not null check(Asthma in ('Yes','No')),
    Hypothyroidism varchar(5) not null check(Hypothyroidism in ('Yes','No')),
    FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID) on delete cascade
);

CREATE TABLE Relative(
	Relative_ID int primary key NOT NULL auto_increment,
    Rel_Name varchar(20) NOT NULL,
    Gender varchar(6) not null check(Gender in ('Male', 'Female', 'Other')),
    relation varchar(20) not null
);

CREATE TABLE Donor(
  Donor_ID int primary key NOT NULL auto_increment,
  Name varchar(20) NOT NULL,
  Date_of_Birth date NOT NULL,
  Gender varchar(6) not null check(Gender in ('Male', 'Female', 'Other')),
  Phone_no char(10),
  EnzymeTest varchar(5) not null check(EnzymeTest in ('Yes','No')),
  BloodTest varchar(5) not null check(BloodTest in ('Yes','No')),
  Address varchar(50),
  organ_donate varchar(20) NOT NULL check(organ_donate in ('lungs', 'pancreas', 'kidney', 'liver')),
  Organization_ID int NOT NULL,
  Relative_ID int,
  FOREIGN KEY(Organization_ID) REFERENCES Organization(organization_ID) on delete cascade,
  Foreign Key(Relative_ID) References Relative(Relative_ID) on delete cascade
);
CREATE TABLE Donor_Medical_History(
    Donor_ID int,
	Diabetes varchar(5) not null check(Diabetes in ('Yes','No')),
    High_Blood_Pressure varchar(5) not null check(High_Blood_Pressure in ('Yes','No')),
    High_Cholesterol varchar(5) not null check(High_Cholesterol in ('Yes','No')),
    Asthma varchar(5) not null check(Asthma in ('Yes','No')),
    Hypothyroidism varchar(5) not null check(Hypothyroidism in ('Yes','No')),
    FOREIGN KEY(Donor_ID) REFERENCES Donor(Donor_ID) on delete cascade
);



CREATE TABLE Future_Donor(
  Future_Donor_ID int primary key NOT NULL auto_increment,
  Name varchar(20) NOT NULL,
  Gender varchar(6) not null check(Gender in ('Male', 'Female', 'Other')),
  Date_of_Birth date NOT NULL,
  Address varchar(50),
  organ varchar(20) NOT NULL check(organ in ('lungs', 'pancreas', 'kidney', 'liver'))
);


CREATE TABLE Organ_available(
  Organ_ID int NOT NULL AUTO_INCREMENT,
  Organ_name varchar(20) NOT NULL,
  Donor_ID int NOT NULL,
  FOREIGN KEY(Donor_ID) REFERENCES Donor(Donor_ID) on delete cascade,
  PRIMARY KEY(Organ_ID)
);

CREATE TABLE Transaction(
  Patient_ID int NOT NULL,
  Organ_ID int NOT NULL,
  Donor_ID int NOT NULL,
  Date_of_transaction date NOT NULL,
  Status int NOT NULL, #0 or 1
  FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID) on delete cascade,
  FOREIGN KEY(Donor_ID) REFERENCES Donor(Donor_ID) on delete cascade,
  PRIMARY KEY(Patient_ID,Organ_ID)
);

create table patient_log(
	querytime datetime,
	comment varchar(255),
    Patient_ID int,
    Name varchar(20) NOT NULL,
    Date_of_Birth date NOT NULL,
    Gender varchar(6) not null check(Gender in ('Male', 'Female', 'Other')),
    Phone_no char(10),
    Address varchar(50),
    organ_req varchar(20) NOT NULL check(organ_req in ('lungs', 'pancreas', 'kidney', 'liver')),
    reason_of_procurement varchar(20),
    Doctor_Name varchar(20) NOT NULL
);

create table donor_log(
  querytime datetime,
  comment varchar(255),
  Donor_ID int,
  Name varchar(20) NOT NULL,
  Date_of_Birth date NOT NULL,
  Gender varchar(6) not null check(Gender in ('Male', 'Female', 'Other')),
  Phone_no char(10),
  EnzymeTest varchar(5) not null check(EnzymeTest in ('Yes','No')),
  BloodTest varchar(5) not null check(BloodTest in ('Yes','No')),
  Address varchar(50),
  organ_donate varchar(20) NOT NULL check(organ_donate in ('lungs', 'pancreas', 'kidney', 'liver')),
  Organization_ID int NOT NULL,
  Relative_ID int
  );
  
create table organ_log(
	querytime datetime,
	comment varchar(255),
    Organ_ID int NOT NULL,
	Organ_name varchar(20) NOT NULL,
	Donor_ID int NOT NULL
);

create table transaction_log(
	querytime datetime,
	comment varchar(255),
    Patient_ID int NOT NULL,
	Organ_ID int NOT NULL,
	Donor_ID int NOT NULL,
	Date_of_transaction date NOT NULL
);

delimiter //
create trigger ADD_DONOR_LOG
after insert
on Donor
for each row
begin
insert into donor_log values
(now(), "Inserted Donor Details : ", new.Donor_ID, new.Name, new.Date_Of_Birth, new.Gender, new.Phone_no, new.EnzymeTest, new.BloodTest, new.Address, new.organ_donate, new.Organization_ID, new.Relative_ID);
end //

delimiter //
create trigger UPD_DONOR_LOG
after update
on Donor
for each row
begin
insert into donor_log values
(now(), "Updated Donor Details : ", new.Donor_ID, new.Name, new.Date_Of_Birth, new.Gender, new.Phone_no, new.EnzymeTest, new.BloodTest, new.Address, new.organ_donate, new.Organization_ID, new.Relative_ID);
end //

delimiter //
create trigger DEL_DONOR_LOG
after delete
on Donor
for each row
begin
insert into donor_log values
(now(), "Deleted Donor Details : ", old.Donor_ID, old.Name, old.Date_Of_Birth, old.Gender, old.Phone_no, old.EnzymeTest, old.BloodTest, old.Address, old.organ_donate, old.Organization_ID, old.Relative_ID);
end //

delimiter //
create trigger ADD_PATIENT_LOG
after insert
on Patient
for each row
begin
insert into patient_log values
(now(), "Inserted new Patient : ", new.Patient_ID, new.Name, new.Date_Of_Birth, new.Gender, new.Phone_no, new.Address, new.organ_req, new.reason_of_procurement, new.Doctor_Name);
end //

delimiter //
create trigger UPD_PATIENT_LOG
after update
on Patient
for each row
begin
insert into patient_log values
(now(), "Updated Patient Details : ", new.Patient_ID, new.Name, new.Date_Of_Birth, new.Gender, new.Phone_no, new.Address, new.organ_req, new.reason_of_procurement, new.Doctor_Name);
end //

delimiter //
create trigger DEL_PATIENT_LOG
after delete
on Patient
for each row
begin
insert into patient_log values
(now(), "Deleted Patient : ", old.Patient_ID, old.Name, old.Date_Of_Birth, old.Gender, old.Phone_no, old.Address, old.organ_req, old.reason_of_procurement, old.Doctor_Name);
end //

delimiter //
create trigger ADD_TRASACTION_LOG
after insert
on Transaction
for each row
begin
insert into transaction_log values
(now(), "Added Transaction : ", new.Patient_ID, new.Organ_ID, new.Donor_ID, new.Date_of_transaction);
end //

delimiter //
create trigger ADD_ORGAN_LOG
after insert
on Organ_Available
for each row
begin
insert into organ_log values
(now(), "Added Organ : ", new.Organ_ID, new.Organ_name, new.Donor_ID);
end //

delimiter //
create procedure add_organ()
begin
declare v_organ varchar(20);
declare v_donor_id int;
declare c1 cursor for select organ_donate, Donor_ID from Donor order by Donor_ID desc limit 1;
open c1;
fetch c1 into v_organ, v_donor_id;
insert into Organ_available (Organ_name, Donor_ID) values(v_organ, v_donor_id);
close c1;
end //


