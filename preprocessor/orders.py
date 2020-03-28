from typing import List
from utils import fetch_json, prefix_dictionary_search, convert_form_to_dict, failover

class Order():
    def __init__(self):
        self._Page = None
        self._Form_dict = None

        self._invoice_number = None
        self._invoice_term_name = None
        self._invoice_date = None

        self._customer_account_number = None
        self._vendor = None
        self._order_items = []
        self._raw_sold_to_info = None

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
    def invoice_term_name(self):
        return self._invoice_term_name

    @property
    def customer_account_number(self):
        return self._customer_account_number

    @property
    def invoice_date(self):
        return self._invoice_date

    @property
    def order_items(self):
        return [order_item for order_item in self._order_items]

    @property
    def raw_sold_to_info(self):
        return self._raw_sold_to_info

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

        # Remove all empty keys
        del matched_keys_raw['']

        return {**matched_keys_raw, **failover(matched_keys_raw, order_template, self._Page)}
    

    def set_order_values(self, page_obj):
        # Set Page object
        self.Page = page_obj
        # Get Page's Form 
        searched_form_dict = self.extract_keys_using_template()
        # Set attributes using matched dict
        # self._customer_account_number = searched_form_dict.get('customer_account_number')
        # self._invoice_date = searched_form_dict.get('invoice_date')
        # self._invoice_term_name = searched_form_dict.get('invoice_term_name')
        # self._raw_sold_to_info = searched_form_dict.get('raw_sold_to_info')
        self.set_attributes(searched_form_dict)

        print(self.__dict__)
        # _temp = self.raw_sold_to_info
        return 

    def set_attributes(self, data):
        for key, val in data.items():
            if hasattr(self, key):
                setattr(self, f'_{key}', val)


