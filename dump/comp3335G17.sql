SET time_zone = "+08:00";

-- CREATE DATABASE comp3335G17;


CREATE TABLE Patients (
  patient_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  date_of_birth DATE NOT NULL,
  contact_information VARCHAR(255) NOT NULL,
  insurance_details VARCHAR(255) NOT NULL,
  username VARCHAR(255) NOT NULL,
  pwHash VARCHAR(255) NOT NULL
);

CREATE TABLE Tests_Catalog (
  test_id INT AUTO_INCREMENT PRIMARY KEY,
  test_code VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  cost DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT NOT NULL,
  test_id INT NOT NULL,
  ordering_physician VARCHAR(255) NOT NULL,
  order_date DATE NOT NULL,
  status VARCHAR(255) NOT NULL,
  FOREIGN KEY (patient_id) REFERENCES Patients (patient_id),
  FOREIGN KEY (test_id) REFERENCES Tests_Catalog (test_id)
);

CREATE TABLE Appointments (
  appointment_id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT NOT NULL,
  appointment_date DATETIME NOT NULL,
  FOREIGN KEY (patient_id) REFERENCES Patients (patient_id)
);

CREATE TABLE Results (
  result_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  report_url VARCHAR(255) NOT NULL,
  interpretation TEXT,
  reporting_pathologist VARCHAR(255) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);

CREATE TABLE Billing (
  bill_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  billed_amount DECIMAL(10, 2) NOT NULL,
  payment_status VARCHAR(255) NOT NULL,
  insurance_claim_status VARCHAR(255) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);

CREATE TABLE Staff (
  staff_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(255) NOT NULL,
  contact_information VARCHAR(255) NOT NULL,
  username VARCHAR(255) NOT NULL,
  pwHash VARCHAR(255) NOT NULL
);

INSERT INTO `Patients` (`name`, `date_of_birth`, `contact_information`, `insurance_details`, `username`, `pwHash`) VALUES
('John Doe', '1990-05-15', 'john@example.com', 'Insurance Company A', 'john_doe', 'password123'),
('Jane Smith', '1985-12-10', 'jane@example.com', 'Insurance Company B', 'jane_smith', 'pass1234'),
('Michael Johnson', '1978-09-20', 'michael@example.com', 'Insurance Company C', 'michael_j', 'pass5678');

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
('Dr. X', 'Physician', 'drx@example.com', 'dr_x', 'pass4321'),
('Dr. Y', 'Pathologist', 'dry@example.com', 'dr_y', 'pass5678'),
('Dr. Z', 'Pathologist', 'drz@example.com', 'dr_z', 'pass9876');
