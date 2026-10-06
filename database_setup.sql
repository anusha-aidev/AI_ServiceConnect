CREATE DATABASE IF NOT EXISTS ai_serviceconnect;
USE ai_serviceconnect;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(15),
    role VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS providers (
    provider_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    service_type VARCHAR(100) NOT NULL,
    experience_years INT DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0.00,
    location VARCHAR(150),
    availability VARCHAR(50) DEFAULT 'Available',
    price_per_hour DECIMAL(10,2),
    verified BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    base_price DECIMAL(10,2),
    category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS service_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    service_id INT,
    request_text TEXT NOT NULL,
    problem_description TEXT,
    location VARCHAR(150),
    urgency VARCHAR(50),
    preferred_date DATE,
    status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (service_id) REFERENCES services(service_id)
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    request_id INT NOT NULL,
    customer_id INT NOT NULL,
    provider_id INT NOT NULL,
    booking_date DATE NOT NULL,
    booking_time TIME,
    status VARCHAR(50) DEFAULT 'Confirmed',
    total_price DECIMAL(10,2),
    FOREIGN KEY (request_id) REFERENCES service_requests(request_id),
    FOREIGN KEY (customer_id) REFERENCES users(user_id),
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    customer_id INT NOT NULL,
    provider_id INT NOT NULL,
    rating INT NOT NULL,
    review_text TEXT,
    review_date DATE,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (customer_id) REFERENCES users(user_id),
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
);

CREATE TABLE IF NOT EXISTS complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    customer_id INT NOT NULL,
    provider_id INT NOT NULL,
    complaint_text TEXT NOT NULL,
    complaint_date DATE,
    status VARCHAR(50) DEFAULT 'Open',
    resolution TEXT,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (customer_id) REFERENCES users(user_id),
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
);

INSERT IGNORE INTO users (name, email, phone, role) VALUES
('Anusha', 'anusha@gmail.com', '9876543210', 'customer'),
('Ravi Kumar', 'ravi@gmail.com', '9876543211', 'provider'),
('Priya Sharma', 'priya@gmail.com', '9876543212', 'provider'),
('Arjun Reddy', 'arjun@gmail.com', '9876543213', 'provider'),
('Sneha Rao', 'sneha@gmail.com', '9876543214', 'provider');

INSERT INTO services (service_name, description, base_price, category)
SELECT 'Plumbing', 'Tap, pipe and water leakage repair', 300.00, 'Home Repair'
WHERE NOT EXISTS (SELECT 1 FROM services WHERE service_name='Plumbing');

INSERT INTO services (service_name, description, base_price, category)
SELECT 'AC Repair', 'AC servicing, cooling and maintenance', 500.00, 'Appliance Repair'
WHERE NOT EXISTS (SELECT 1 FROM services WHERE service_name='AC Repair');

INSERT INTO services (service_name, description, base_price, category)
SELECT 'Electrical', 'Electrical wiring, switches and repair', 350.00, 'Home Repair'
WHERE NOT EXISTS (SELECT 1 FROM services WHERE service_name='Electrical');

INSERT INTO services (service_name, description, base_price, category)
SELECT 'Home Cleaning', 'Complete home cleaning service', 400.00, 'Home Care'
WHERE NOT EXISTS (SELECT 1 FROM services WHERE service_name='Home Cleaning');

INSERT INTO services (service_name, description, base_price, category)
SELECT 'Home Tutor', 'Personalized academic tutoring', 500.00, 'Education'
WHERE NOT EXISTS (SELECT 1 FROM services WHERE service_name='Home Tutor');

INSERT INTO providers
(user_id, service_type, experience_years, rating, location, availability, price_per_hour, verified)
SELECT 2, 'AC Repair', 5, 4.80, 'Hyderabad', 'Available', 500.00, TRUE
WHERE NOT EXISTS (SELECT 1 FROM providers WHERE user_id=2);

INSERT INTO providers
(user_id, service_type, experience_years, rating, location, availability, price_per_hour, verified)
SELECT 3, 'Plumbing', 7, 4.60, 'Hyderabad', 'Available', 350.00, TRUE
WHERE NOT EXISTS (SELECT 1 FROM providers WHERE user_id=3);

INSERT INTO providers
(user_id, service_type, experience_years, rating, location, availability, price_per_hour, verified)
SELECT 4, 'Electrical', 4, 4.50, 'Hyderabad', 'Available', 400.00, TRUE
WHERE NOT EXISTS (SELECT 1 FROM providers WHERE user_id=4);

INSERT INTO providers
(user_id, service_type, experience_years, rating, location, availability, price_per_hour, verified)
SELECT 5, 'Home Cleaning', 3, 4.70, 'Hyderabad', 'Available', 450.00, TRUE
WHERE NOT EXISTS (SELECT 1 FROM providers WHERE user_id=5);
