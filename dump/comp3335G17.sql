SET time_zone = "+08:00";

CREATE TABLE Patients (
  patient_id INT AUTO_INCREMENT PRIMARY KEY,
  name varbinary(512) DEFAULT NULL, -- encrypted
  date_of_birth DATE NOT NULL,
  contact_information varbinary(512) DEFAULT NULL, -- encrypted
  insurance_details varbinary(512) DEFAULT NULL, -- encrypted
  username VARCHAR(255) NOT NULL,
  pwHash VARCHAR(255) NOT NULL,
  enc_iv binary(16) DEFAULT NULL -- for encryption
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Tests_Catalog (
  test_id INT AUTO_INCREMENT PRIMARY KEY,
  test_code VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  cost DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT NOT NULL,
  test_id INT NOT NULL,
  ordering_physician VARCHAR(255) NOT NULL,
  order_date DATE NOT NULL,
  status VARCHAR(255) NOT NULL,
  FOREIGN KEY (patient_id) REFERENCES Patients (patient_id),
  FOREIGN KEY (test_id) REFERENCES Tests_Catalog (test_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Appointments (
  appointment_id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT NOT NULL,
  appointment_date DATETIME NOT NULL,
  FOREIGN KEY (patient_id) REFERENCES Patients (patient_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Results (
  result_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  report_url VARCHAR(255) NOT NULL, -- not encrypted since we assume that the report is encrypted
  interpretation TEXT,
  reporting_pathologist VARCHAR(255) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES Orders (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Billing (
  bill_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  billed_amount DECIMAL(10, 2) NOT NULL,
  payment_status VARCHAR(255) NOT NULL,
  insurance_claim_status VARCHAR(255) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES Orders (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Staff (
  staff_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(255) NOT NULL,
  contact_information varbinary(512) DEFAULT NULL, -- encrypted
  username VARCHAR(255) NOT NULL,
  pwHash VARCHAR(255) NOT NULL,
  enc_iv binary(16) DEFAULT NULL -- for encryption
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET block_encryption_mode = 'aes-256-cbc';
SET @key_str = 'My secret passphrase';

SET @init_vector = RANDOM_BYTES(16);
SET @init_vector1 = RANDOM_BYTES(16);
SET @init_vector2 = RANDOM_BYTES(16);

INSERT INTO `Patients` (`name`, `date_of_birth`, `contact_information`, `insurance_details`,`enc_iv`, `username`, `pwHash`) VALUES
(AES_ENCRYPT('John Doe', @key_str, @init_vector, "hkdf"), '1990-05-15', AES_ENCRYPT('john@example.com', @key_str, @init_vector, "hkdf"), AES_ENCRYPT('Insurance Company A', @key_str, @init_vector, "hkdf"), @init_vector, 'john_doe', 'pbkdf2:sha256:600000$2GQOX8fIBMPODxuL$237b5461860bcc8cee64b11e49f3b54eb9d0e5b4116b108e2765ffce0f593753'),
(AES_ENCRYPT('Jane Smith', @key_str, @init_vector1, "hkdf"), '1985-12-10', AES_ENCRYPT('jane@example.com', @key_str, @init_vector1, "hkdf"), AES_ENCRYPT('Insurance Company B', @key_str, @init_vector1, "hkdf"), @init_vector1, 'jane_smith', 'pbkdf2:sha256:600000$woyBKh5CUmAx7azh$9d8c951ca72e28b2d372cff2b8dd501c38e1e247f178d1bf49b0b3f004089ea9'),
(AES_ENCRYPT('Michael Johnson', @key_str, @init_vector2, "hkdf"), '1978-09-20', AES_ENCRYPT('michael@example.com', @key_str, @init_vector2, "hkdf"), AES_ENCRYPT('Insurance Company C', @key_str, @init_vector2, "hkdf"), @init_vector2, 'michael_j', 'pbkdf2:sha256:600000$ZoQIW7oqjx1bdDw7$091b7f9bf86a54ed905ffd75e586ff02dd56438cb8e1a1ad0d51d6eb95c34d63');

INSERT INTO Tests_Catalog (test_code, name, description, cost) VALUES
('T001', 'Blood Test', 'Complete blood count and basic metabolic panel', 100.00),
('T002', 'Urinalysis', 'Analysis of urine sample for various parameters', 50.00),
('T003', 'Cholesterol Test', 'Measure lipid levels in the blood', 80.00);

INSERT INTO Orders (patient_id, test_id, ordering_physician, order_date, status) VALUES
(1, 1, 'Dr. X', '2023-11-01', 'Pending'),
(2, 2, 'Dr. X', '2023-11-02', 'Completed'),
(3, 3, 'Dr. Y', '2023-11-03', 'Pending');

INSERT INTO Appointments (patient_id, appointment_date) VALUES
(1, '2023-11-05 09:00:00'),
(2, '2023-11-06 10:30:00'),
(3, '2023-11-07 14:00:00');

INSERT INTO Results (order_id, report_url, interpretation, reporting_pathologist) VALUES
(1, 'https://example.com/reports/1', 'Normal blood test results', 'Dr. Y'),
(2, 'https://example.com/reports/2', 'Abnormal urine analysis results', 'Dr. Y'),
(3, 'https://example.com/reports/3', 'High cholesterol levels', 'Dr. Z');

INSERT INTO Billing (order_id, billed_amount, payment_status, insurance_claim_status) VALUES
(1, 100.00, 'Paid', 'Claimed'),
(2, 50.00, 'Paid', 'Claimed'),
(3, 80.00, 'Pending', 'Not Claimed');

INSERT INTO Staff (name, role, contact_information, username, pwHash) VALUES
('Dr. X', 'lab_staff', AES_ENCRYPT('drx@example.com', @key_str, @init_vector, "hkdf"), 'dr_x', 'pbkdf2:sha256:600000$CoZpPPiPWZqFznXT$91554f9882e5651136118192f5341ed556ae67e428e36f5aafb98bb5a7cd7222'),
('Dr. Y', 'lab_staff', AES_ENCRYPT('dryy@example.com', @key_str, @init_vector, "hkdf"), 'dr_y', 'pbkdf2:sha256:600000$RS0hz9L6okiWjUIO$e2cb5a18a258441fd6288fc1d75f0e0cee44e41c8ac3dd580f1da6e3a937b1d5'),
('Dr. Z', 'secretaries', AES_ENCRYPT('drz@example.com', @key_str, @init_vector, "hkdf"), 'dr_z', 'pbkdf2:sha256:600000$MGCXJdZyDky4PigO$e179df88dfce16b2919b1a96925e4a0bbea760bce27eb3b7aa09215795e47665');

-- DROP FUNCTION IF EXISTS F_AES_DECRYPT
-- CREATE FUNCTION F_AES_DECRYPT(PID INT) RETURNS VARCHAR
-- BEGIN
--     RETURN SELECT AES_DECRYPT(enc_data, @key_str, enc_iv, "hkdf") FROM data; 
-- END;

-- Create the role
CREATE ROLE 'lab_staff', 'secretaries', 'patients';

-- Grant table privileges
GRANT SELECT, INSERT, UPDATE ON myDb.Orders TO lab_staff;
GRANT SELECT, INSERT, UPDATE ON myDb.Results TO lab_staff;

GRANT SELECT, INSERT, UPDATE ON myDb.Appointments TO secretaries;
GRANT SELECT, INSERT, UPDATE ON myDb.Billing TO secretaries;
GRANT SELECT ON myDb.Orders TO secretaries;
GRANT SELECT ON myDb.Results TO secretaries;

GRANT SELECT ON myDb.Orders TO patients;
GRANT SELECT ON myDb.Results TO patients;
GRANT SELECT ON myDb.Billing TO patients;
GRANT SELECT (test_id, name, description) ON myDb.Tests_Catalog TO patients;

-- create general type of users
CREATE USER 'LS' IDENTIFIED BY 'lab_staff';
CREATE USER 'SE' IDENTIFIED BY 'secretaries';
CREATE USER 'PA' IDENTIFIED BY 'patients';

GRANT 'lab_staff' to 'LS';
GRANT 'secretaries' to 'SE';
GRANT 'patients' to 'PA';
-- GRANT EXECUTE ON F_AES_DECRYPT to 'PA';

SET DEFAULT ROLE 'lab_staff' TO 'LS';
SET DEFAULT ROLE 'secretaries' TO 'SE';
SET DEFAULT ROLE 'patients' TO 'PA';

FLUSH PRIVILEGES;
