-- Forty-five products cover three pages at the default twenty-item block size.
-- All prices use THB. No user sessions or carts are seeded.
SET TIME ZONE 'UTC';
BEGIN;

INSERT INTO currencies(code, name, symbol) VALUES ('THB', 'Thai Baht', '฿');
INSERT INTO categories(code) VALUES ('home'), ('book'), ('notebook'), ('office'), ('electronics');
INSERT INTO tags(code) VALUES ('month-offers'), ('best-sellers'), ('home'), ('discount-10perc'), ('study');

INSERT INTO products(code, name, description, unit_price, currency_id)
SELECT seed.code, seed.name, seed.description, seed.unit_price, currency.id
FROM (VALUES
    ('HOME-ABC-001', 'Adjustable Desk Lamp', 'A warm white LED lamp with an adjustable arm for a reading desk.', 690.00),
    ('HOME-ABC-002', 'Bamboo Storage Tray', 'A reusable tray for organising small household objects.', 249.50),
    ('HOME-ABC-003', 'Ceramic Coffee Mug', 'A plain ceramic mug with a comfortable handle.', 129.00),
    ('HOME-ABC-004', 'Cotton Cushion Cover', 'A washable cushion cover for a sofa or reading chair.', 179.00),
    ('HOME-ABC-005', 'Desk Clock', 'A compact clock with an easy-to-read dial.', 399.00),
    ('HOME-ABC-006', 'Glass Water Bottle', 'A reusable bottle with a protective fabric sleeve.', 289.00),
    ('HOME-ABC-007', 'Kitchen Measuring Set', 'A set of measuring spoons and cups for home cooking.', 159.00),
    ('HOME-ABC-008', 'Linen Table Runner', 'A neutral table runner for a small dining table.', 459.00),
    ('HOME-ABC-009', 'Plant Pot', 'A small indoor plant pot with a matching saucer.', 199.00),
    ('BOOK-ABC-001', 'API Design Workbook', 'Practice exercises for designing clear service interfaces.', 520.00),
    ('BOOK-ABC-002', 'Architecture Sketchbook', 'A guided workbook for sketching software architecture.', 375.00),
    ('BOOK-ABC-003', 'Database Basics', 'An introductory guide to relational data and queries.', 450.00),
    ('BOOK-ABC-004', 'Design Patterns Guide', 'An illustrated introduction to common object-oriented patterns.', 650.00),
    ('BOOK-ABC-005', 'Everyday Python', 'Small Python exercises for everyday programming tasks.', 495.00),
    ('BOOK-ABC-006', 'HTTP Field Notes', 'A concise reference for HTTP methods and response codes.', 325.00),
    ('BOOK-ABC-007', 'Practical Testing', 'A workbook on meaningful tests and readable assertions.', 580.00),
    ('BOOK-ABC-008', 'Service Design Primer', 'A beginner-friendly guide to service responsibilities.', 610.00),
    ('BOOK-ABC-009', 'Web Accessibility Notes', 'Examples of accessible forms and navigation patterns.', 420.00),
    ('NOTE-ABC-001', 'A4 Grid Notebook', 'A grid notebook for diagrams and calculations.', 89.00),
    ('NOTE-ABC-002', 'A5 Dotted Notebook', 'A dotted notebook for planning and lecture notes.', 119.00),
    ('NOTE-ABC-003', 'Blue Pocket Notebook', 'A pocket notebook with a blue cover.', 59.00),
    ('NOTE-ABC-004', 'Daily Planner', 'An undated planner for daily goals and appointments.', 219.00),
    ('NOTE-ABC-005', 'Hardcover Journal', 'A ruled journal with a durable hard cover.', 249.00),
    ('NOTE-ABC-006', 'Index Card Pack', 'A pack of cards for revision and presentation notes.', 49.00),
    ('NOTE-ABC-007', 'Project Logbook', 'A notebook with sections for decisions and progress.', 169.00),
    ('NOTE-ABC-008', 'Recycled Paper Pad', 'A writing pad made with recycled paper.', 79.00),
    ('NOTE-ABC-009', 'Weekly Study Planner', 'A planner for organising a weekly study schedule.', 139.00),
    ('OFFICE-ABC-001', 'Ballpoint Pen Set', 'A set of black and blue pens for daily writing.', 69.00),
    ('OFFICE-ABC-002', 'Binder Clip Pack', 'Reusable metal clips for grouping loose papers.', 39.00),
    ('OFFICE-ABC-003', 'Cork Notice Board', 'A compact board for reminders and course schedules.', 349.00),
    ('OFFICE-ABC-004', 'Document Folder', 'A folder for carrying printed coursework.', 45.00),
    ('OFFICE-ABC-005', 'Eraser and Pencil Set', 'A simple pencil set for sketches and written exercises.', 55.00),
    ('OFFICE-ABC-006', 'Highlighter Pack', 'Four coloured highlighters for marking study notes.', 99.00),
    ('OFFICE-ABC-007', 'Metal Ruler', 'A thirty-centimetre ruler for accurate lines.', 65.00),
    ('OFFICE-ABC-008', 'Sticky Note Set', 'Assorted sticky notes for temporary reminders.', 75.00),
    ('OFFICE-ABC-009', 'Whiteboard Marker Set', 'Three dry-erase markers for classroom exercises.', 149.00),
    ('ELEC-ABC-001', 'Bluetooth Speaker', 'A compact portable speaker for a study room.', 1290.00),
    ('ELEC-ABC-002', 'Cable Organiser', 'Reusable clips for keeping desk cables tidy.', 95.00),
    ('ELEC-ABC-003', 'Compact Keyboard', 'A wired keyboard with a space-saving layout.', 790.00),
    ('ELEC-ABC-004', 'Laptop Stand', 'A folding stand that raises a laptop screen.', 890.00),
    ('ELEC-ABC-005', 'Mouse Pad', 'A plain fabric mouse pad with a non-slip base.', 109.00),
    ('ELEC-ABC-006', 'USB Desk Fan', 'A small USB-powered fan for a desk.', 359.00),
    ('ELEC-ABC-007', 'USB Hub', 'A four-port USB hub for everyday peripherals.', 490.00),
    ('ELEC-ABC-008', 'Webcam Cover', 'A sliding cover for a laptop camera.', 29.00),
    ('ELEC-ABC-009', 'Wired Mouse', 'A comfortable wired mouse for everyday computer use.', 299.00)
) AS seed(code, name, description, unit_price)
CROSS JOIN currencies currency WHERE currency.code = 'THB';

INSERT INTO product_categories(product_id, category_id)
SELECT p.id, c.id FROM products p JOIN categories c ON c.code =
    CASE split_part(p.code, '-', 1)
        WHEN 'HOME' THEN 'home' WHEN 'BOOK' THEN 'book'
        WHEN 'NOTE' THEN 'notebook' WHEN 'OFFICE' THEN 'office'
        WHEN 'ELEC' THEN 'electronics' END;

-- Every product has at least one tag. Each home-page group has nine or more.
INSERT INTO product_tags(product_id, tag_id)
SELECT p.id, t.id FROM products p CROSS JOIN tags t
WHERE (t.code = 'home' AND p.code LIKE 'HOME-%')
   OR (t.code = 'month-offers' AND right(p.code, 3)::integer <= 3)
   OR (t.code = 'best-sellers' AND right(p.code, 3)::integer BETWEEN 3 AND 5)
   OR (t.code = 'discount-10perc' AND right(p.code, 3)::integer = 2)
   OR (t.code = 'study' AND p.code NOT LIKE 'HOME-%');

COMMIT;
