-- ==========================================
-- Week 1 CS Core: Database Normalization (SQLite Compatible)
-- ==========================================

-- 1. UNNORMALIZED TABLE
CREATE TABLE book_orders (
    order_id INT, customer_name VARCHAR(100), customer_email VARCHAR(100),
    customer_address VARCHAR(255), book_isbn VARCHAR(20), book_title VARCHAR(200),
    book_author VARCHAR(100), book_price DECIMAL(10, 2), order_date DATE,
    quantity INT, total_price DECIMAL(10, 2)
);

INSERT INTO book_orders VALUES
(1, 'John Smith', 'john@example.com', '123 Main St', '978-0141439518', 'Pride and Prejudice', 'Jane Austen', 9.99, '2023-01-15', 1, 9.99),
(2, 'John Smith', 'john@example.com', '123 Main St', '978-0451524935', '1984', 'George Orwell', 12.99, '2023-01-15', 2, 25.98),
(3, 'Mary Johnson', 'mary@example.com', '456 Oak Ave', '978-0061120084', 'To Kill a Mockingbird', 'Harper Lee', 14.99, '2023-01-20', 1, 14.99),
(4, 'Robert Brown', 'robert@example.com', '789 Pine Rd', '978-0141439518', 'Pride and Prejudice', 'Jane Austen', 9.99, '2023-01-25', 1, 9.99);

-- 2. FIRST NORMAL FORM (1NF)
CREATE TABLE book_orders_1nf (
    order_id INT, customer_name VARCHAR(100), customer_email VARCHAR(100),
    customer_address VARCHAR(255), book_isbn VARCHAR(20), book_title VARCHAR(200),
    book_author VARCHAR(100), book_price DECIMAL(10, 2), order_date DATE,
    quantity INT, total_price DECIMAL(10, 2),
    PRIMARY KEY (order_id, book_isbn)
);

-- 3. SECOND NORMAL FORM (2NF) - Removes partial dependencies
CREATE TABLE orders_2nf (
    order_id INT PRIMARY KEY, customer_name VARCHAR(100),
    customer_email VARCHAR(100), customer_address VARCHAR(255), order_date DATE
);

CREATE TABLE books_2nf (
    isbn VARCHAR(20) PRIMARY KEY, title VARCHAR(200),
    author VARCHAR(100), price DECIMAL(10, 2)
);

CREATE TABLE order_items_2nf (
    order_id INT, book_isbn VARCHAR(20), quantity INT, total_price DECIMAL(10, 2),
    PRIMARY KEY (order_id, book_isbn),
    FOREIGN KEY (order_id) REFERENCES orders_2nf(order_id),
    FOREIGN KEY (book_isbn) REFERENCES books_2nf(isbn)
);

INSERT INTO orders_2nf VALUES
(1, 'John Smith', 'john@example.com', '123 Main St', '2023-01-15'),
(2, 'John Smith', 'john@example.com', '123 Main St', '2023-01-15'),
(3, 'Mary Johnson', 'mary@example.com', '456 Oak Ave', '2023-01-20'),
(4, 'Robert Brown', 'robert@example.com', '789 Pine Rd', '2023-01-25');

INSERT INTO books_2nf VALUES
('978-0141439518', 'Pride and Prejudice', 'Jane Austen', 9.99),
('978-0451524935', '1984', 'George Orwell', 12.99),
('978-0061120084', 'To Kill a Mockingbird', 'Harper Lee', 14.99);

INSERT INTO order_items_2nf VALUES
(1, '978-0141439518', 1, 9.99),
(2, '978-0451524935', 2, 25.98),
(3, '978-0061120084', 1, 14.99),
(4, '978-0141439518', 1, 9.99);

-- 4. THIRD NORMAL FORM (3NF) - Removes transitive dependencies
CREATE TABLE customers_3nf (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite syntax
    customer_name TEXT, email TEXT, address TEXT
);

CREATE TABLE orders_3nf (
    order_id INT PRIMARY KEY, customer_id INT, order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers_3nf(customer_id)
);

CREATE TABLE books_3nf (
    isbn VARCHAR(20) PRIMARY KEY, title VARCHAR(200),
    author VARCHAR(100), price DECIMAL(10, 2)
);

CREATE TABLE order_items_3nf (
    order_id INT, book_isbn VARCHAR(20), quantity INT,
    PRIMARY KEY (order_id, book_isbn),
    FOREIGN KEY (order_id) REFERENCES orders_3nf(order_id),
    FOREIGN KEY (book_isbn) REFERENCES books_3nf(isbn)
);

-- FIXED: using customer_name instead of name
INSERT INTO customers_3nf (customer_name, email, address) VALUES
('John Smith', 'john@example.com', '123 Main St'),
('Mary Johnson', 'mary@example.com', '456 Oak Ave'),
('Robert Brown', 'robert@example.com', '789 Pine Rd');

INSERT INTO orders_3nf VALUES
(1, 1, '2023-01-15'),
(2, 2, '2023-01-20'),
(3, 3, '2023-01-25');

INSERT INTO books_3nf VALUES
('978-0141439518', 'Pride and Prejudice', 'Jane Austen', 9.99),
('978-0451524935', '1984', 'George Orwell', 12.99),
('978-0061120084', 'To Kill a Mockingbird', 'Harper Lee', 14.99);

INSERT INTO order_items_3nf VALUES
(1, '978-0141439518', 1),
(1, '978-0451524935', 2),
(2, '978-0061120084', 1),
(3, '978-0141439518', 1);

-- FIXED: using c.customer_name in the SELECT
SELECT
    o.order_id, c.customer_name, b.title AS book_title,
    oi.quantity, (oi.quantity * b.price) AS total_price
FROM orders_3nf o
JOIN customers_3nf c ON o.customer_id = c.customer_id
JOIN order_items_3nf oi ON o.order_id = oi.order_id
JOIN books_3nf b ON oi.book_isbn = b.isbn;
