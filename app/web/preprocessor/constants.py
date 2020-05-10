TEMPLATES_DIR = './web/preprocessor/templates/'

SPREADERS = ['description']

REGEX_MAP = {
	"float": "[-+]?\d*\.?\d+|$",
	# "float"
	# [-+] # option magnitude sign
	# ?\d*\.\d+ # should always contain starting digit(s) with decimal followed by some more digit(s)
	# 
	"int": "[-]?[0-9]+|$"
	# "int"
	# [-] # option for negative sign
	# ?[0-9]+ # can contain one or more digits
	# 
}

# Required to create tsv files in the right order
ORDERITEMS_COLUMN_ORDER = ['account_number' , 
							'organization_number' ,
							'invoice_number' ,
							'item_number' ,
							'order_quantity' ,
							'shipped_quantity',
							'size' ,
							'measure', 
							'broken' ,
							'unit' ,
							'brand' ,
							'description', 
							'weight', 
							'price',
							'total_price',
							's3_image_key']

ORDER_HEADER_COLUMN_ORDER = ['account_number' ,
							'organization_number',
							'invoice_number' ,
							'invoice_term_name' ,
							'invoice_date' ,
							'customer_account_number' ,
							'invoice_subtotal' ,
							'sold_to']

DB_DATE_FORMAT = "%Y-%m-%d"