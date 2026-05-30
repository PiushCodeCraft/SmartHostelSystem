-- ============================================================
--  Smart Hostel System — MySQL Schema
--  Run this file once to set up your database:
--  mysql -u root -p < database/hostel.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS smart_hostel;
USE smart_hostel;

-- ── Students ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    student_id    VARCHAR(20)  UNIQUE NOT NULL,   -- e.g. STU001
    first_name    VARCHAR(50)  NOT NULL,
    last_name     VARCHAR(50)  NOT NULL,
    roll_number   VARCHAR(20)  UNIQUE NOT NULL,
    class         VARCHAR(30)  NOT NULL,
    gender        ENUM('Male','Female','Other') DEFAULT 'Male',
    dob           DATE,
    guardian_name VARCHAR(100),
    guardian_phone VARCHAR(20),
    guardian_email VARCHAR(100),
    address       TEXT,
    photo_path    VARCHAR(255),
    notes         TEXT,
    is_active     TINYINT(1)   DEFAULT 1,
    created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- ── Attendance ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS attendance (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    student_id    VARCHAR(20)  NOT NULL,
    date          DATE         NOT NULL,
    check_in      TIME,
    check_out     TIME,
    location      VARCHAR(100) DEFAULT 'Main Gate',
    status        ENUM('Present','Absent','Late') DEFAULT 'Present',
    UNIQUE KEY uq_student_date (student_id, date),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- ── Unknown Faces ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS unknown_faces (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    detected_at   DATETIME     DEFAULT CURRENT_TIMESTAMP,
    location      VARCHAR(100),
    camera        VARCHAR(50),
    confidence    FLOAT,
    image_path    VARCHAR(255),
    is_resolved   TINYINT(1)   DEFAULT 0,
    resolved_at   DATETIME,
    notes         TEXT
);

-- ── System Logs ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS system_logs (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    timestamp     DATETIME     DEFAULT CURRENT_TIMESTAMP,
    level         ENUM('INFO','WARN','ERROR') DEFAULT 'INFO',
    source        VARCHAR(100),
    message       TEXT
);

-- ── Cameras ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cameras (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    camera_name   VARCHAR(50)  UNIQUE NOT NULL,
    location      VARCHAR(100),
    status        ENUM('Online','Offline') DEFAULT 'Online',
    last_ping     DATETIME     DEFAULT CURRENT_TIMESTAMP,
    ip_address    VARCHAR(50)
);

-- ── Location Status ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS location_status (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(100) UNIQUE NOT NULL,
    current_count INT          DEFAULT 0,
    capacity      INT          DEFAULT 100,
    status        ENUM('Open','Locked','Restricted') DEFAULT 'Open',
    updated_at    DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ── Admin Users ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS admin_users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(30)  DEFAULT 'admin',
    created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
--  SAMPLE DATA
-- ============================================================

-- Students
INSERT IGNORE INTO students (student_id, first_name, last_name, roll_number, class, gender, dob, guardian_name, guardian_phone, address) VALUES
('STU001','Aarav','Mehta',   'A-01','Class A','Male',  '2005-03-12','Raj Mehta',   '+91 98765 43210','123 MG Road, Bengaluru'),
('STU002','Priya','Sharma',  'B-04','Class B','Female','2005-07-22','Sunita Sharma','+91 91234 56789','45 Park Street, Mumbai'),
('STU003','Rahul','Nair',    'A-07','Class A','Male',  '2004-11-05','Suresh Nair',  '+91 99887 76655','78 Beach Road, Kochi'),
('STU004','Ananya','Patel',  'C-02','Class C','Female','2006-01-18','Amit Patel',   '+91 87654 32109','22 Gandhi Nagar, Ahmedabad'),
('STU005','Kiran','Reddy',   'B-09','Class B','Male',  '2005-09-30','Venkat Reddy', '+91 76543 21098','9 Jubilee Hills, Hyderabad'),
('STU006','Diya','Joshi',    'C-11','Class C','Female','2006-04-14','Meera Joshi',  '+91 65432 10987','56 FC Road, Pune'),
('STU007','Rohan','Iyer',    'A-12','Class A','Male',  '2004-12-25','Ravi Iyer',    '+91 54321 09876','34 Anna Nagar, Chennai'),
('STU008','Sneha','Kulkarni','B-02','Class B','Female','2005-06-08','Priya Kulkarni','+91 43210 98765','67 Koregaon Park, Pune');

-- Attendance (today)
INSERT IGNORE INTO attendance (student_id, date, check_in, status) VALUES
('STU001', CURDATE(), '09:02:00', 'Present'),
('STU002', CURDATE(), '08:55:00', 'Present'),
('STU003', CURDATE(), NULL,       'Absent'),
('STU004', CURDATE(), '09:11:00', 'Present'),
('STU005', CURDATE(), '08:48:00', 'Present'),
('STU006', CURDATE(), NULL,       'Absent'),
('STU007', CURDATE(), '09:05:00', 'Present'),
('STU008', CURDATE(), '09:18:00', 'Present');

-- Attendance (last 7 days for chart)
INSERT IGNORE INTO attendance (student_id, date, check_in, status) VALUES
('STU001', DATE_SUB(CURDATE(),INTERVAL 1 DAY), '08:50:00', 'Present'),
('STU002', DATE_SUB(CURDATE(),INTERVAL 1 DAY), '09:00:00', 'Present'),
('STU003', DATE_SUB(CURDATE(),INTERVAL 1 DAY), '09:10:00', 'Present'),
('STU001', DATE_SUB(CURDATE(),INTERVAL 2 DAY), '08:45:00', 'Present'),
('STU002', DATE_SUB(CURDATE(),INTERVAL 2 DAY), '08:55:00', 'Present'),
('STU001', DATE_SUB(CURDATE(),INTERVAL 3 DAY), '09:00:00', 'Present'),
('STU003', DATE_SUB(CURDATE(),INTERVAL 3 DAY), '09:20:00', 'Late');

-- Unknown Faces
INSERT IGNORE INTO unknown_faces (detected_at, location, camera, confidence, is_resolved) VALUES
(NOW() - INTERVAL 2 HOUR,  'Corridor C',  'Cam 5', 91.2, 0),
(NOW() - INTERVAL 4 HOUR,  'Main Gate',   'Cam 1', 87.5, 0),
(NOW() - INTERVAL 6 HOUR,  'Library',     'Cam 8', 94.1, 1),
(NOW() - INTERVAL 8 HOUR,  'Cafeteria',   'Cam 4', 82.3, 1);

-- System Logs
INSERT IGNORE INTO system_logs (timestamp, level, source, message) VALUES
(NOW() - INTERVAL 10 MINUTE, 'ERROR', 'camera-gateB',   'Connection timeout – no heartbeat'),
(NOW() - INTERVAL 25 MINUTE, 'WARN',  'cafeteria-cam',  'Occupancy threshold exceeded'),
(NOW() - INTERVAL 40 MINUTE, 'INFO',  'camera-3',       'Stream reconnected successfully'),
(NOW() - INTERVAL 1 HOUR,    'INFO',  'reports-engine', 'Monthly report generated'),
(NOW() - INTERVAL 2 HOUR,    'WARN',  'face-detect',    'Unknown face in Corridor C (conf 91%)'),
(NOW() - INTERVAL 3 HOUR,    'INFO',  'system',         'Routine health check passed'),
(NOW() - INTERVAL 4 HOUR,    'INFO',  'gate-A',         'Student recognised: Aarav Mehta'),
(NOW() - INTERVAL 5 HOUR,    'ERROR', 'db-conn',        'Slow query warning – 2400ms');

-- Cameras
INSERT IGNORE INTO cameras (camera_name, location, status, ip_address) VALUES
('Cam 1', 'Main Gate',   'Online',  '192.168.1.101'),
('Cam 2', 'Corridor A',  'Online',  '192.168.1.102'),
('Cam 3', 'Library',     'Online',  '192.168.1.103'),
('Cam 4', 'Cafeteria',   'Online',  '192.168.1.104'),
('Cam 5', 'Corridor C',  'Online',  '192.168.1.105'),
('Cam 6', 'Parking Lot', 'Online',  '192.168.1.106'),
('Cam 7', 'Server Room', 'Online',  '192.168.1.107'),
('Cam 8', 'Gate B',      'Offline', '192.168.1.108');

-- Location Status
INSERT IGNORE INTO location_status (location_name, current_count, capacity, status) VALUES
('Main Entrance', 0,  0,   'Open'),
('Gate B',        0,  0,   'Locked'),
('Library',       42, 80,  'Open'),
('Cafeteria',     78, 100, 'Open'),
('Parking Lot',   23, 40,  'Open'),
('Server Room',   0,  0,   'Open');

-- Admin user (password: admin123)
INSERT IGNORE INTO admin_users (username, password_hash, role) VALUES
('admin', 'admin123', 'Super Admin'),

