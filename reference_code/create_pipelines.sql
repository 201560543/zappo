-- Pipeline Creation
CREATE OR REPLACE PIPELINE order_headers_s3
AS LOAD DATA S3 'invoiceupload-memsql/export/header'
CONFIG '{"region": "us-west-2"}'
INTO TABLE `invoice_header_final_test`
FIELDS TERMINATED BY '\t'
(`account_number`, `invoice_number`, `invoice_term_name`, `invoice_date`, `supplier`, `customer_account_number`, `sold_to`);

CREATE OR REPLACE PIPELINE order_lineitems_s3
AS LOAD DATA S3 'invoiceupload-memsql/export/lineitem'
CONFIG '{"region": "us-west-2"}'
INTO TABLE `invoice_lineitem_final_test`
FIELDS TERMINATED BY '\t'
(`account_number`, `supplier`, `invoice_number`, `item_number`, `order_quantity`, `shipped_quantity`, `size`, `measure`, 
    `broken`, `unit`, `brand`, `description`, `weight`, `price`, `total_price`);

-- See what files are picked up
SELECT * FROM information_schema.PIPELINES_FILES;

-- Reset and run pipelines in background
DELETE FROM invoice_header_final_test;
ALTER PIPELINE order_headers_s3 SET OFFSETS EARLIEST;
START PIPELINE order_headers_s3;

DELETE FROM invoice_lineitem_final_test;
ALTER PIPELINE order_lineitems_s3 SET OFFSETS EARLIEST;
START PIPELINE order_lineitems_s3;

-- Stop pipeline commands
STOP PIPELINE order_headers_s3;
STOP PIPELINE order_lineitems_s3
