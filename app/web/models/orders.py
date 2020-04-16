from flask_sqlalchemy import SQLAlchemy
from web import db
from web.preprocessor.utils import fetch_json, prefix_dictionary_search, convert_form_to_dict, failover

class Order(db.Model):
    invoice_number = db.Column(db.String(32), primary_key = True)
    invoice_term_name = db.Column(db.String(32))
    invoice_date = db.Column(db.String(32))

    customer_account_number = db.Column(db.String(32))
    vendor = db.Column(db.String(32))
    order_items = db.Column(db.String(32))
    raw_sold_to_info = db.Column(db.String(32))

    def __init__(self):
        self._Page = None
        self._Form_dict = None

    def __repr__(self):
        return '<Order {0}>'.format(self.invoice_number)

    def add_order_items(self, order_item):
        self._order_items.append(order_item)

    def extract_keys_using_template(self, template_name = 'sysco.json'):
        """
        Extract keys from Page object's Form Fields, search template for matches, and return matches with their corresponding indices
        """
        # Fetch the required template type
        template_data = fetch_json(template_name)
        # Fetch the order item template
        order_template = template_data.get('mapper').get('order')
        # For each extracted key, search for relevant keys from the json template
        matched_keys_raw = {prefix_dictionary_search(field_key, order_template):self.Form_dict[field_key]
                            for field_key, val
                            in self.Form_dict.items()
                            if val is not None}

        # Remove all empty keys
        del matched_keys_raw['']

        return {**matched_keys_raw, **failover(matched_keys_raw, order_template, self._Page)}
    

    def set_order_values(self, page_obj, template_name = 'sysco.json'):
        # Set Page object
        self.Page = page_obj
        # Get Page's Form 
        searched_form_dict = self.extract_keys_using_template(template_name)
        # Set attributes using matched dict
        # self._customer_account_number = searched_form_dict.get('customer_account_number')
        # self._invoice_date = searched_form_dict.get('invoice_date')
        # self._invoice_term_name = searched_form_dict.get('invoice_term_name')
        # self._raw_sold_to_info = searched_form_dict.get('raw_sold_to_info')
        self.set_attributes(searched_form_dict)

        print(self.__dict__)
        return 

    def set_attributes(self, data):
        for key, val in data.items():
            if hasattr(self, key):
                setattr(self, f'_{key}', val)
