from typing import List
from utils import fetch_json, prefix_dictionary_search, convert_form_to_dict

class Order():
    def __init__(self):
        self._Page = None
        self._Form_dict = None
        self._invoice_number = None
        self._customer_accnt_no = None
        self._vendor = None
        self._order_items = []

    def __str__(self):
        return f'{self._invoice_number}, number of items: {len(self._order_items)}'

    @property
    def Page(self):
        return self._Page
	
    @Page.setter
    def Page(self,page_obj):
        self._Page = page_obj
        self._Form_dict = convert_form_to_dict(page_obj.form)

    @property
    def Form_dict(self):
        return self._Form_dict

    @property
    def invoice_number(self):
        return self._invoice_number

    @property
    def customer_accnt_no(self):
        return self._customer_accnt_no

    @property
    def order_items(self):
        return [order_item for order_item in self._order_items]

    @property
    def vendor(self):
        return self._vendor

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
                            for field_key 
                            in self.Form_dict.keys()}
        
        return matched_keys_raw
    



    def set_order_values(self, page_obj):
        # Set Page object
        self.Page = page_obj
        # Get Page's Form 
        self.extract_keys_using_template()

