-- Create pipelines
-- Pipeline Creation
CREATE OR REPLACE PIPELINE order_headers_s3
AS LOAD DATA S3 'invoiceupload-memsql/export/header'
CONFIG '{"region": "us-west-2"}'
INTO TABLE `invoice_header_import`
IGNORE 1 LINES
FIELDS TERMINATED BY '\t'
(`account_number`, `organization_number`, `invoice_number`, `invoice_term_name`, `invoice_date`, `customer_account_number`, `sold_to`);

CREATE OR REPLACE PIPELINE order_lineitems_s3
AS LOAD DATA S3 'invoiceupload-memsql/export/lineitem'
CONFIG '{"region": "us-west-2"}'
INTO TABLE `invoice_lineitem_import`
IGNORE 1 LINES
FIELDS TERMINATED BY '\t'
(`account_number`, `organization_number`, `invoice_number`, `item_number`, `order_quantity`, `shipped_quantity`, `size`, `measure`, 
    `broken`, `unit`, `brand`, `description`, `weight`, `price`, `total_price`,`s3_image_key`);

-- See what files are picked up
SELECT * FROM information_schema.PIPELINES_FILES;

-- Reset and run pipelines in background
DELETE FROM invoice_header_final_test;
ALTER PIPELINE order_headers_s3 SET OFFSETS EARLIEST;
START PIPELINE order_headers_s3;

DELETE FROM invoice_lineitem_final_test;
ALTER PIPELINE order_lineitems_s3 SET OFFSETS EARLIEST;
START PIPELINE order_lineitems_s3;

-- Stop and drop pipeline commands
STOP PIPELINE order_headers_s3;
STOP PIPELINE order_lineitems_s3;

DROP PIPELINE order_headers_s3;
DROP PIPELINE order_lineitems_s3;