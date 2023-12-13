-- This script creates a trigger that decreases the quantity of an item after adding a new order.
-- Quantity in the table items can be negative.

-- clear existing trigger
DROP TRIGGER IF EXISTS update_inventory;

DELIMITER $$
CREATE TRIGGER update_inventory
AFTER INSERT
ON orders FOR EACH ROW
BEGIN
        UPDATE items
        SET quantity = quantity - NEW.number
        WHERE items.name = NEW.item_name;
END;
$$
DELIMITER ;
