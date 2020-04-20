create table if not exists invoice_header_final_test (
    account_number varchar(35),
    invoice_number int,
    invoice_term_name varchar(30),
    invoice_date date,
    supplier varchar(15),
    customer_account_number int,
    sold_to varchar(100)
);


create table if not exists invoice_lineitem_final_test (
    account_number varchar(35),
    supplier varchar(15),
    invoice_number int,
    item_number int,
    order_quantity int,
    shipped_quantity int,
    size varchar(10),
    measure varchar(10),
    broken char(1),
    unit int,
    brand varchar(30),
    description varchar(100),
    weight decimal(6,2),
    price decimal(7,2),
    total_price decimal(7,2)
);
