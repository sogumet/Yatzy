--
-- DDL for database yatzy
--
USE yatzy;
-- Drop tables in order to avoid FK constraint
DROP TABLE IF EXISTS score;


-- Create table scoreboard
CREATE TABLE score
(
    id INT AUTO_INCREMENT NOT NULL,
    time_created DATE DEFAULT CURRENT_DATE,
    namn CHAR(16) NOT NULL,
    total INT,

    PRIMARY KEY (id),
    KEY (namn)
);

--Create view all score
DROP VIEW IF EXISTS v_all_score;
CREATE VIEW v_all_score
AS
SELECT
    namn,
    time_created AS Tid,
    total
FROM
	score
ORDER BY total desc;

--Create procedure view all score
DROP PROCEDURE IF EXISTS show_all_score;
    DELIMITER ;;
CREATE PROCEDURE show_all_score()
BEGIN
    SELECT * FROM v_all_score;
END
;;
DELIMITER ;

/* - Create table highscore
CREATE TABLE higscore
(
    id INT UNIQUE,
    namn INT DEFAULT 0,
    -
    FOREIGN KEY (id) REFERENCES scoreboard(id) 
);

-- Create table frys 2
CREATE TABLE frys_2
(
    product INT UNIQUE,
    kilo INT DEFAULT 0,
    
    FOREIGN KEY (product) REFERENCES product(id) 
);

-- Create table frys 3
CREATE TABLE frys_3
(
    product INT UNIQUE,
    kilo INT DEFAULT 0,
    
    FOREIGN KEY (product) REFERENCES product(id) 
);

-- Create table kund
CREATE TABLE kund
(
    id INT AUTO_INCREMENT NOT NULL,
    fornamn CHAR(11),
    efternamn CHAR(16),
    adress CHAR(40),
    telefon CHAR(16),

    PRIMARY KEY (id),
    KEY (efternamn)
);

-- Create table kategori
CREATE TABLE kategori
(
	id INT AUTO_INCREMENT NOT NULL,
    kategori CHAR(16),
    PRIMARY KEY (id)
);

-- Create table kategori_2
CREATE TABLE kategori_2
(
    product INT,
    kategori INT,
    FOREIGN KEY (product) REFERENCES product(id),
    FOREIGN KEY (kategori) REFERENCES kategori(id)
);

-- Create table order
CREATE TABLE orders
(
    id INT AUTO_INCREMENT NOT NULL,
    kund INT,
    rader INT DEFAULT 0,
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_updated TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    time_delivered TIMESTAMP NULL,
    time_deleted TIMESTAMP NULL,
    time_ordered TIMESTAMP NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (kund) REFERENCES kund(id)
);

-- Create table order_rad
CREATE TABLE order_rad
(
    id INT AUTO_INCREMENT NOT NULL,
    orders INT,
    product INT,
    items INT,
    rest INT DEFAULT 0,

    PRIMARY KEY (id),
    FOREIGN KEY (orders) REFERENCES orders(id),
    FOREIGN KEY (product) REFERENCES product(id)
);

-- Create table faktura
CREATE TABLE faktura
(
    id INT AUTO_INCREMENT NOT NULL,
    orders INT,
    kund INT,
    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_paid DATE NULL,
    total_price FLOAT DEFAULT 0,

    PRIMARY KEY (id),
    FOREIGN KEY (orders) REFERENCES orders(id),
    FOREIGN KEY (kund) REFERENCES kund(id)
);

-- Create table faktura_rad
CREATE TABLE faktura_rad
(
    id INT AUTO_INCREMENT NOT NULL,
    orders INT,
    produkt INT,
    items INT,
    rest INT,
    price FLOAT,

    PRIMARY KEY (id),
    FOREIGN KEY (orders) REFERENCES orders(id),
    FOREIGN KEY (produkt) REFERENCES product(id)
);

-- Create procedure for select kategori from kategorí
DROP PROCEDURE IF EXISTS show_kategori;
DELIMITER ;;
CREATE PROCEDURE show_kategori()
BEGIN
    SELECT kategori FROM kategori;
END
;;
DELIMITER ;


-- View products plus lager
DROP VIEW IF EXISTS v_product_lager;
CREATE VIEW v_product_lager
AS
SELECT
p.id,
p.namn,
p.beskrivning,
p.pris,

coalesce(a.kilo, 0) +
coalesce(b.kilo, 0) +
coalesce(c.kilo, 0) as kilo
FROM product AS p
	LEFT JOIN frys_1 AS a
	ON p.id = a.product
		LEFT JOIN frys_2 AS b
		on p.id = b.product
			LEFT JOIN frys_3 AS c
			ON p.id = c.product
ORDER BY p.id
;

-- Create view product plus kategori
DROP VIEW IF EXISTS v_product_kategori;
CREATE VIEW v_product_kategori
AS
SELECT
	k2.product,
	k.kategori   
FROM kategori AS k
    JOIN kategori_2 AS k2
        ON k.id = k2.kategori
        order by product
;

-- Create view product plus kategori
DROP VIEW IF EXISTS v_product_kategorier;
CREATE VIEW v_product_kategorier
AS
SELECT product,
GROUP_CONCAT(kategori) AS kategori
from v_product_kategori
GROUP BY product;

-- Create view product total
DROP VIEW IF EXISTS v_main_product;
CREATE VIEW v_main_product
AS
SELECT
    p.id,
	p.namn,
    p.beskrivning,
    p.pris,
    p.kilo,
    k.kategori
FROM
	v_product_lager AS p
	LEFT JOIN v_product_kategorier AS k
			ON k.product = p.id
ORDER BY id
;

-- Procedure show_main_products()
DROP PROCEDURE IF EXISTS show_main_products;
    DELIMITER ;;
CREATE PROCEDURE show_main_products()
BEGIN
    SELECT * FROM v_main_product;
END
;;
DELIMITER ;

-- Procedure show categories
DROP PROCEDURE IF EXISTS show_categories;
	DELIMITER ;;
CREATE PROCEDURE show_categories()
BEGIN
	SELECT kategori FROM kategori;
END
;;
DELIMITER ;

-- Procedure show one product
DROP PROCEDURE IF EXISTS show_one_product;
	DELIMITER ;;
CREATE PROCEDURE show_one_product(a_id INT)
BEGIN
	SELECT * FROM v_main_product
    WHERE a_id = id;
END
;;
DELIMITER ;


-- Procedure for edit product details
DROP PROCEDURE IF EXISTS edit_product;
DELIMITER ;;
CREATE PROCEDURE edit_product(
    a_id INT,
    a_namn CHAR(16),
    a_beskrivning CHAR(100),
    a_pris FLOAT
)
BEGIN
    UPDATE product SET
        `namn` = a_namn,
        `beskrivning` = a_beskrivning,
        `pris` = a_pris

    WHERE
        `id` = a_id;
END
;;
DELIMITER ;

-- Create procedure for insert into product
DROP PROCEDURE IF EXISTS insert_product;
DELIMITER ;;

CREATE PROCEDURE insert_product(
    a_namn CHAR(16),
    a_beskrivning CHAR(100),
    a_pris FLOAT
)
BEGIN
    INSERT INTO product (namn, beskrivning, pris)
    VALUES (a_namn, a_beskrivning, a_pris);
END
;;
DELIMITER ;


-- Create procedure delete product
DROP PROCEDURE IF EXISTS delete_product;
DELIMITER ;;
CREATE PROCEDURE delete_product(
	a_id INT
    )
BEGIN
DELETE  FROM frys_1
    WHERE product = a_id;
DELETE  FROM frys_2
    WHERE product = a_id;
DELETE  FROM frys_3
    WHERE product = a_id;
DELETE FROM kategori_2    
    WHERE product = a_id;
DELETE FROM product
	WHERE id = a_id;
END
;;
DELIMITER ;

-- Log product table
CREATE TABLE log_product
(
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `clock` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `what` CHAR(40)
    
);
-- Trigger for logging insert product
DROP TRIGGER IF EXISTS log_product_insert;

CREATE TRIGGER log_product_insert
AFTER INSERT
ON product FOR EACH ROW
    INSERT INTO log_product (`what`)
        VALUE (concat("En produkt med id " , NEW.id, " lades till."));
        
-- Trigger for logging update product
DROP TRIGGER IF EXISTS log_product_update;

CREATE TRIGGER log_product_update
AFTER UPDATE
ON product FOR EACH ROW
    INSERT INTO log_product (`what`)
        VALUE (concat("Produkten med id " , OLD.id, " uppdaterades."));

-- Trigger for logging delete product
DROP TRIGGER IF EXISTS log_product_delete;

CREATE TRIGGER log_product_delete
BEFORE DELETE
ON product FOR EACH ROW
    INSERT INTO log_product (`what`)
        VALUE (concat("Produkten med id " , OLD.id, " togs bort."));

-- Procedure for showing log_product
DROP PROCEDURE IF EXISTS show_log_product;

DELIMITER ;;

CREATE PROCEDURE show_log_product
(a_number INT)
BEGIN 
	SELECT id, 
    DATE_FORMAT(clock, "%a %b %d %H:%i:%s") as clock, 
    what from log_product
    ORDER BY id DESC
    LIMIT a_number;
END
;;
DELIMITER ;


--View to show inventory
DROP VIEW IF EXISTS v_show_inventory;
CREATE VIEW v_show_inventory
AS
SELECT * FROM
(
SELECT
    p.id,
    p.namn,
	coalesce(a.kilo, 0) as frys_1,
    coalesce(b.kilo, 0) as frys_2,
    coalesce(c.kilo, 0) as frys_3,
    coalesce(a.kilo, 0) + coalesce(b.kilo, 0) + coalesce(c.kilo, 0) as total
	
FROM
	product AS p
		LEFT JOIN frys_1 AS a 
		ON p.id = a.product
            LEFT JOIN frys_2 AS b 
			ON p.id = b.product
				LEFT JOIN frys_3 AS c 
				ON p.id = c.product
)
as t
ORDER BY t.id;

-- Procedure to show inventory
DROP PROCEDURE IF EXISTS show_inventory;
    DELIMITER ;;
CREATE PROCEDURE show_inventory()
BEGIN
    SELECT * FROM v_show_inventory;
END
;;
DELIMITER ;

-- Procedure to search lager
DROP PROCEDURE IF EXISTS lager_search;
DELIMITER ;;
CREATE PROCEDURE lager_search(
    a_wild CHAR(18)
)
BEGIN
    SELECT * FROM
        v_show_inventory
    AS lagerfilter
    WHERE id LIKE a_wild OR namn LIKE a_wild OR 
	    frys_1 LIKE a_wild OR frys_2 LIKE a_wild OR 
        frys_3 LIKE a_wild;
END
;;
DELIMITER ;

-- Procedure to add product in frys_1
DROP PROCEDURE IF EXISTS update_frys_1;
    DELIMITER ;;
CREATE PROCEDURE update_frys_1(
    a_id INT,
    a_value INT
)
BEGIN
    INSERT INTO frys_1
    VALUES (a_id, a_value)
    ON DUPLICATE KEY UPDATE kilo = kilo + a_value;
END
;;
DELIMITER ;

-- Procedure to add product in frys_2
DROP PROCEDURE IF EXISTS update_frys_2;
    DELIMITER ;;
CREATE PROCEDURE update_frys_2(
    a_id INT,
    a_value INT
)
BEGIN
    INSERT INTO frys_2
    VALUES (a_id, a_value)
    ON DUPLICATE KEY UPDATE kilo = kilo + a_value;
END
;;
DELIMITER ;

-- Procedure to add product in frys_3
DROP PROCEDURE IF EXISTS update_frys_3;
    DELIMITER ;;
CREATE PROCEDURE update_frys_3(
    a_id INT,
    a_value INT
)
BEGIN
    INSERT INTO frys_3
    VALUES (a_id, a_value)
    ON DUPLICATE KEY UPDATE kilo = kilo + a_value;
END
;;
DELIMITER ;

-- Procedure to reduce product in frys_1
DROP PROCEDURE IF EXISTS reduce_frys_1;
    DELIMITER ;;
CREATE PROCEDURE reduce_frys_1(
    a_id INT,
    a_value INT
)
BEGIN
    update frys_1
    SET kilo = kilo - a_value
    WHERE product = a_id;
END
;;
DELIMITER ;

-- Procedure to add reduce product in frys_2
DROP PROCEDURE IF EXISTS reduce_frys_2;
    DELIMITER ;;
CREATE PROCEDURE reduce_frys_2(
    a_id INT,
    a_value INT
)
BEGIN
    update frys_2
    SET kilo = kilo - a_value
    WHERE product = a_id;
END
;;
DELIMITER ;

-- Procedure to reduce product in frys_3
DROP PROCEDURE IF EXISTS reduce_frys_3;
    DELIMITER ;;
CREATE PROCEDURE reduce_frys_3(
    a_id INT,
    a_value INT
)
BEGIN
    update frys_3
    SET kilo = kilo - a_value
    WHERE product = a_id;
END
;;
DELIMITER ;

-- Procedure to show products in category
DROP PROCEDURE IF EXISTS show_products_in_category;
DELIMITER ;;
CREATE PROCEDURE show_products_in_category (
a_category CHAR(16)
)
BEGIN
SELECT
	id, 
	namn,
    pris
FROM product AS p
JOIN (
	SELECT
	product FROM kategori_2
	WHERE kategori = (
		SELECT
		id FROM kategori
		WHERE kategori = a_category
			)
		)
AS k ON p.id = k.product
;
END
;;
DELIMITER ;

-- Create update kategori procedure
DROP PROCEDURE IF EXISTS update_category;
    DELIMITER ;;
CREATE PROCEDURE update_category(
    a_id INT,
    a_kategori INT
)
BEGIN
    INSERT INTO kategori_2
    VALUES (a_id, a_kategori);
END
;;
DELIMITER ;

-- Create procedure show kunder
DROP PROCEDURE IF EXISTS show_kund;
DELIMITER ;;
CREATE PROCEDURE show_kund()
BEGIN
SELECT * FROM kund
;
END
;;
DELIMITER ;

-- Create procedure show one kund
DROP PROCEDURE IF EXISTS show_one_kund;
DELIMITER ;;
CREATE PROCEDURE show_one_kund(
    a_id INT
)
BEGIN
SELECT * FROM kund
WHERE id = a_id
;
END
;;
DELIMITER ;

-- Procedure create order
DROP PROCEDURE IF EXISTS create_order;
DELIMITER ;;
CREATE PROCEDURE create_order (
	a_kund INT
)
BEGIN
INSERT INTO orders(
    kund 
)
VALUES (
	a_kund)
;
END
;;
DELIMITER ;

-- Create procedure show_one_order
DROP PROCEDURE IF EXISTS show_one_order;
DELIMITER ;;
CREATE PROCEDURE show_one_order(
a_id INT
)
BEGIN
SELECT
    o.id AS order_id,
	sum_rader(a_id) AS rader, 
	k.fornamn, 
	k.efternamn,
    k.id AS kund_id,
    order_status(
        o.time_deleted,
        o.time_delivered,
        o.time_ordered,
        o.time_updated,
        o.time_created
    ) as statuz 	
FROM kund AS k
JOIN orders AS o ON k.id = o.kund
WHERE o.id = a_id; 
END
;;
DELIMITER ;

-- Create procedure show_orders
DROP PROCEDURE IF EXISTS show_orders;
DELIMITER ;;
CREATE PROCEDURE show_orders()
BEGIN
SELECT
    o.id AS order_id,
	rader, 
	k.fornamn, 
	k.efternamn,
    k.id AS kund_id,
    DATE_FORMAT(o.time_created, "%y-%m-%e %H:%i:%d") AS time_created,
    order_status(
        o.time_deleted,
        o.time_delivered,
        o.time_ordered,
        o.time_updated,
        o.time_created
    ) as statuz
FROM kund AS k
JOIN orders AS o ON k.id = o.kund;
END
;;
DELIMITER ;

-- Procedure create orderrad
DROP PROCEDURE IF EXISTS create_order_row;
DELIMITER ;;
CREATE PROCEDURE create_order_row(
    a_order INT,
    a_product INT,
    a_items INT
)
BEGIN
INSERT INTO order_rad(
    orders,
    product,
    items
)
VALUES (
	a_order,
    a_product,
    a_items
)
;
END
;;
DELIMITER ;

-- Function to sum rader per order in orderrad
DROP FUNCTION IF EXISTS sum_rader;
DELIMITER ;;
CREATE FUNCTION sum_rader(
	a_order INT
)
RETURNS INT
DETERMINISTIC
BEGIN
	DECLARE rader INT;
	SELECT count(orders)
    INTO rader
	FROM order_rad
    WHERE orders = a_order;
	
RETURN rader;
END
;;
DELIMITER ;

-- Procedure visar alla rader i en order
DROP PROCEDURE IF EXISTS show_order_rader;
DELIMITER ;;
CREATE PROCEDURE show_order_rader(
a_order INT
)
BEGIN
SELECT
	p.id,
	p.namn,
	p.pris,
    r.items,
    r.id as radid
FROM product AS p
JOIN order_rad AS r
	ON r.product = p.id
    WHERE r.orders = a_order;
END
;;
DELIMITER ;

-- Trigger for logging orderrows
DROP TRIGGER IF EXISTS log_order_rad_insert;

CREATE TRIGGER log_order_rad_insert
AFTER INSERT
ON order_rad FOR EACH ROW
    UPDATE  orders SET rader = sum_rader(orders.id) 
        WHERE NEW.orders = orders.id;

-- Create function order_status
DROP FUNCTION IF EXISTS order_status;
DELIMITER ;;
CREATE FUNCTION order_status(
    time_deleted TIMESTAMP,
    time_delivered TIMESTAMP,
    time_ordered TIMESTAMP,
    time_updated TIMESTAMP,
    time_created TIMESTAMP
)
RETURNS CHAR(12)
DETERMINISTIC
BEGIN
    IF time_deleted IS NOT NULL THEN
        RETURN 'Raderad';
    ELSEIF time_delivered IS NOT NULL THEN
        RETURN 'Skickad';
    ELSEIF time_ordered IS NOT NULL THEN
        RETURN 'Bestalld';
    ELSEIF time_updated IS NOT NULL THEN
        RETURN 'Uppdaterad';
    ELSEIF time_created IS NOT NULL THEN
        RETURN 'Skapad';
    END IF;
END
;;

DELIMITER ;

-- Procedure make beställd
DROP PROCEDURE IF EXISTS bestall;
DELIMITER ;;
CREATE PROCEDURE bestall(
a_id INT
)
BEGIN
UPDATE orders
SET
    time_ordered = current_timestamp
WHERE
    id = a_id;
END
;;
DELIMITER ;

--Procedure search orders
DROP PROCEDURE IF EXISTS search_orders;
DELIMITER ;;
CREATE PROCEDURE search_orders(
    a_id INT
)
BEGIN
SELECT
    o.id AS order_id,
	rader, 
	k.fornamn, 
	k.efternamn,
    k.id AS kund_id,
    DATE_FORMAT(o.time_created, "%y-%m-%d %H:%i") AS time_created,
    order_status(
        o.time_deleted,
        o.time_delivered,
        o.time_ordered,
        o.time_updated,
        o.time_created
    ) as statuz
FROM kund AS k
JOIN orders AS o ON k.id = o.kund
WHERE a_id = o.id OR a_id = k.id;
END
;;
DELIMITER ;

--Function plocklista
DROP FUNCTION IF EXISTS pick_list;
DELIMITER ;;
CREATE FUNCTION pick_list(
    frys_1 INT,
    frys_2 INT,
    frys_3 INT
)

RETURNS CHAR(55)
DETERMINISTIC

BEGIN
    DECLARE frys1 CHAR(55);
    DECLARE frys2 CHAR(55);
    DECLARE frys3 CHAR(55);
	DECLARE ampty CHAR(55);
    SET ampty = "Inte i lager";
	set frys1 = concat("Frys 1: ",cast(frys_1 as char), " kg ");
	set frys2 = concat(" Frys 2: ",cast(frys_2 as char), " kg ");
    set frys3 = concat(" Frys 3: ",cast(frys_3 as char), " kg");
    IF frys_1 + frys_2 + frys_3 = 0 THEN
		RETURN ampty;
	ELSE 
		RETURN concat(frys1, frys2, frys3);
	END IF;
END
;;
DELIMITER ;

--Procedur plocklista alla rader
DROP PROCEDURE IF EXISTS pick_list_all;
DELIMITER ;;
CREATE PROCEDURE pick_list_all(
a_order INT
)
BEGIN
SELECT
	p.id,
	p.namn,
    r.items,
    a_order,
(SELECT ifnull((select pick_list(
frys_1,
frys_2,
frys_3 
)FROM
v_show_inventory
WHERE id = p.id), "Inte i lager")) AS lager_status
FROM product AS p
JOIN order_rad AS r
	ON r.product = p.id
    WHERE r.orders = a_order;
END
;;
DELIMITER ; 

-- Procedure make order skickad
DROP PROCEDURE IF EXISTS order_delivered;
DELIMITER ;;
CREATE PROCEDURE order_delivered(
a_id INT
)
BEGIN
UPDATE orders
SET
    time_delivered = current_timestamp
WHERE
    id = a_id;
END
;;
DELIMITER ;

-- Show one product in lager
DROP PROCEDURE IF EXISTS show_inven_one_prod;
	DELIMITER ;;
CREATE PROCEDURE show_inven_one_prod (
	a_id INT
)
BEGIN
	select * from v_show_inventory
	where id = a_id;
END
;;
DELIMITER ;

-- Procedure to make a faktura
DROP PROCEDURE IF EXISTS create_faktura;
	DELIMITER ;;
CREATE PROCEDURE create_faktura (
	a_id INT
)
BEGIN
	insert INTO faktura( orders, kund)
select
id, kund
from orders
where id = a_id;
END
;;
DELIMITER ;

-- Procedure to make fakturarad
DROP PROCEDURE IF EXISTS create_faktura_rad;
	DELIMITER ;;
CREATE PROCEDURE create_faktura_rad (
	a_id INT
)
BEGIN
	insert INTO faktura_rad( orders, produkt, items, rest, price)
select
o.orders, 
o.product,
o.items,
o.rest,
(SELECT pris FROM
product where o.product = id) 
from order_rad as o
where o.orders = a_id;
END
;;
DELIMITER ;

-- Procedur update rest in order_rad
DROP PROCEDURE IF EXISTS update_rest_order_rad;
	DELIMITER ;;
CREATE PROCEDURE update_rest_order_rad (
	a_id INT,
    a_rest INT
)
BEGIN
	update order_rad
    SET rest = a_rest
    WHERE id = a_id;
END
;;
DELIMITER ;

-- View calculated fakturarad
DROP VIEW IF EXISTS v_calculated_faktura_rad;
CREATE VIEW v_calculated_faktura_rad
AS SELECT 
	orders,
    produkt,
    (select namn from product where produkt = id) as namn,
    items - rest as items,
    price as pris,
    (items - rest) * price as summa
FROM faktura_rad
WHERE (items - rest) <> 0;

-- Create function faktura_status
DROP FUNCTION IF EXISTS faktura_status;
DELIMITER ;;
CREATE FUNCTION faktura_status(
    time_paid TIMESTAMP
)
RETURNS CHAR(12)
DETERMINISTIC
BEGIN
    IF time_paid IS NOT NULL THEN
        RETURN 'Betald';
    ELSE
        RETURN 'Ej betald';
    END IF;
END
;;

DELIMITER ;

-- Procedure to get orders
DROP PROCEDURE IF EXISTS get_invoices;
DELIMITER ;;
CREATE PROCEDURE get_invoices()
BEGIN
SELECT 
	f.id as faktura_id,
    f.orders as order_id,
	k.fornamn,
	k.efternamn,
	k.id AS kundid,
	DATE_FORMAT(f.time_created, "%y-%m-%d %H:%i") AS time_created,
	faktura_status(f.time_paid) as status
FROM faktura as f JOIN kund AS k
ON f.kund = K.id
ORDER BY f.id;
END
;;
DELIMITER ;

--Function to get faktura summa
DROP FUNCTION IF EXISTS sum_faktura;
DELIMITER ;;
CREATE FUNCTION sum_faktura(
	a_faktura INT
)
RETURNS FLOAT
DETERMINISTIC
BEGIN
	DECLARE sum FLOAT;
	SELECT sum(summa)
    INTO sum
	FROM v_calculated_faktura_rad
    WHERE orders = a_faktura;
RETURN sum;
END
;;
DELIMITER ;

-- Procedur update rest in order_rad
DROP PROCEDURE IF EXISTS get_faktura_head;
	DELIMITER ;;
CREATE PROCEDURE get_faktura_head (
	a_id INT
)
BEGIN
	SELECT
		f.id AS faktura_id,
        a_id AS order_id,
		k.id AS kund_id,
		k.fornamn,
		k.efternamn,
		k.adress,
		sum_faktura(a_id) as summa,
		faktura_status(p.time_paid) as status
	FROM faktura_rad AS f
		JOIN kund AS k 
	ON f.id = k.id
		JOIN faktura as p
	ON p.id = f.id	
    WHERE p.orders = a_id;    
END
;;
DELIMITER ;

-- Procedure get fakturarader
DROP PROCEDURE IF EXISTS get_faktura_rader;
	DELIMITER ;;
CREATE PROCEDURE get_faktura_rader(
	a_id INT
)
BEGIN
	SELECT 
		produkt,
		namn,
		items,
		pris,
		summa
	FROM v_calculated_faktura_rad
	WHERE orders = a_id;
END
;;
DELIMITER ;

-- Procedure set faktura to paid
DROP PROCEDURE IF EXISTS pay_faktura;
	DELIMITER ;;
CREATE PROCEDURE pay_faktura(
	a_id INT,
    a_date DATE
)
BEGIN
	UPDATE faktura
SET time_paid = a_date
WHERE id = a_id; 
END
;;
DELIMITER ;
 */