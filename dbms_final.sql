CREATE DATABASE new_dbms;
USE new_dbms; 

CREATE TABLE login(
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL
);

INSERT INTO login VALUES ('admin','admin');

CREATE TABLE Patient(
	Patient_ID int primary key NOT NULL auto_increment ,
    Name varchar(20) NOT NULL,
    Date_of_Birth date NOT NULL,
    Medical_insurance int,
    Medical_history varchar(20),
    Street varchar(20),
    City varchar(20),
    State varchar(20),
    organ_req varchar(20) NOT NULL check(organ_req in ('lungs', 'eyes', 'heart')),
    reason_of_procurement varchar(20),
    Doctor_ID int NOT NULL,
    FOREIGN KEY(Doctor_ID) REFERENCES Doctor(Doctor_ID) ON DELETE CASCADE
);

CREATE TABLE Patient_emergency_phone(
    Patient_ID int NOT NULL,
    emergency_no varchar(15),
    FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID) ON DELETE CASCADE
);

CREATE TABLE Donor(
  Donor_ID int primary key NOT NULL auto_increment,
  Name varchar(20) NOT NULL,
  Date_of_Birth date NOT NULL,
  Medical_insurance int,
  Medical_history varchar(20),
  Street varchar(20),
  City varchar(20),
  State varchar(20),
  organ_donated varchar(20) NOT NULL check(organ_donated in ('lungs', 'eyes', 'heart')),
  date_of_death date not null,
  Organization_ID int NOT NULL,
  FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE
);

CREATE TABLE Donor_emergency_phone(
    Donor_ID int NOT NULL,
    emergency_no varchar(15),
    FOREIGN KEY(Donor_ID) REFERENCES Donor(Donor_ID) ON DELETE CASCADE
);

CREATE TABLE Organ_available(
  Organ_ID int NOT NULL AUTO_INCREMENT,
  Organ_name varchar(20) NOT NULL,
  Donor_ID int NOT NULL,
  FOREIGN KEY(Donor_ID) REFERENCES Donor(Donor_ID) ON DELETE CASCADE,
  PRIMARY KEY(Organ_ID)
);

CREATE TABLE Transaction(
  Patient_ID int NOT NULL,
  Organ_ID int NOT NULL,
  Donor_ID int NOT NULL,
  Date_of_transaction date NOT NULL,
  Status int NOT NULL, #0 or 1
  FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID) ON DELETE CASCADE,
  FOREIGN KEY(Donor_ID) REFERENCES Donor(Donor_ID) ON DELETE CASCADE,
  PRIMARY KEY(Patient_ID,Organ_ID)
);

CREATE TABLE Organization(
  Organization_ID int NOT NULL,
  Organization_name varchar(20) NOT NULL,
  Location varchar(20),
  Government_approved int, # 0 or 1
  PRIMARY KEY(Organization_ID)
);

CREATE TABLE Doctor(
  Doctor_ID int NOT NULL AUTO_INCREMENT,
  Doctor_Name varchar(20) NOT NULL,
  Department_Name varchar(20) NOT NULL,
  organization_ID int NOT NULL,
  FOREIGN KEY(organization_ID) REFERENCES Organization(organization_ID) ON DELETE CASCADE,
  PRIMARY KEY(Doctor_ID)
);

CREATE TABLE Organization_phone_no(
  Organization_ID int NOT NULL,
  Phone_no varchar(15),
  FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE
);

CREATE TABLE Doctor_phone_no(
  Doctor_ID int NOT NULL,
  Phone_no varchar(15),
  FOREIGN KEY(Doctor_ID) REFERENCES Doctor(Doctor_ID) ON DELETE CASCADE
);

CREATE TABLE Organization_head(
  Organization_ID int NOT NULL,
  Employee_ID int NOT NULL,
  Name varchar(20) NOT NULL,
  Date_of_joining date NOT NULL,
  Term_length int NOT NULL,
  FOREIGN KEY(Organization_ID) REFERENCES Organization(Organization_ID) ON DELETE CASCADE,
  PRIMARY KEY(Organization_ID,Employee_ID)
);

create table log (
  querytime datetime,
  comment varchar(255)
);

