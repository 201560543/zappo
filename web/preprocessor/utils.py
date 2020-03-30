import json
import re
import pandas as pd
from typing import Dict, List
from constants import TEMPLATES_DIR, SPREADERS

def find(s: str, ch: str) -> List:
	"""
	Utility function to find all indexes of a character in a string
	"""
	return [i for i, ltr in enumerate(s) if ltr == ch]

def fetch_json(template_name: str) -> Dict:
	"""
	Fetches the json file and returns it. This lookup is done through the template name
	"""
	try:
		with open(f'{TEMPLATES_DIR}/{template_name}') as f:
			return json.load(f)
	except IOError:
		print(f'File {template_name} does not exist')


def prefix_search(prefix: str, template_data: Dict) -> List:
	return [(key, val) for key, val in template_data.items()  
                   if key.startswith(prefix)]

def remove_special_characters(text, extra_attr=''):
	"""
	Remove special characters
	"""
	return re.sub(f'[^A-Za-z0-9 {extra_attr}]+', '', text)

def prefix_dictionary_search(key: str, template_data: Dict) -> str:
	"""
	Checks which key matches with present json 
	"""
	# Smart check to check if the value matches together
	clean_key = remove_special_characters(key)

	find_all_spaces = find(clean_key, ' ')

	find_all_spaces.append(len(clean_key))

	print('c', clean_key)
	if clean_key in template_data:
		return template_data[clean_key]

	for index in find_all_spaces:
		prefix = clean_key[:index]
		print(prefix)

		matched_items = prefix_search(prefix, template_data)

		if len(matched_items) == 1:
			return matched_items[0][1]

	return ''


def missing_headers(current_data, template_data):
    """
    Returns columns which could not be found in the key value pair
    """
    missed_headers = [key for key, val in template_data.items() if val not in current_data]
    return missed_headers

def fetch_page_lines(lines, missing_header):
    for line in lines:
        line_text = remove_special_characters(line.text).lower().strip()
        if line_text == missing_header:
            return next(lines).text


def failover(current_data, template_data, page_obj):
    missed_headers = missing_headers(current_data, template_data)

    if not missed_headers:
        return {}

    return {
        template_data[missed_header]: fetch_page_lines(page_obj.lines, missed_header)
        for missed_header in missed_headers
    }


def spread_columns(df):
	index_map = {col: index for index, col in enumerate(df.columns)}
	col_names = df.columns

	for spreader in SPREADERS:
		if spreader in index_map:
			start_point = index_map[spreader]
			for left_index in range(start_point-1, -1, -1):
				if col_names[left_index] != '':
					break
				df[spreader] = df.iloc[:, left_index].astype(str)+" "+df[spreader]

			for right_index in range(start_point+1, len(col_names)):
				if col_names[right_index] != '':
					break
				df[spreader] = df[spreader]+" "+df.iloc[:, right_index].astype(str)

	return df

def update_column_headers(df, template_name='sysco.json'):
    column_headers = df.iloc[0]
    # Strip all whitespaces and change to lowercase
    column_headers = [header.strip().lower() for header in column_headers]
    # Fetch the required template type
    template_data = fetch_json(template_name)
    # Fetch the order item template
    order_item_template = template_data.get('mapper').get('order_item')
    # Fetch the column headers
    column_headers = [prefix_dictionary_search(header, order_item_template) for header in column_headers]
    # Return the correct dataframe with changed column headers
    orders_df = pd.DataFrame(df.values[1:], columns=column_headers)
    # Spread the columns if they are empty
    orders_df = spread_columns(orders_df)

    if '' in orders_df:
	    orders_df.drop([''], axis = 1, inplace=True) 

    return orders_df

def convert_form_to_dict(form_obj):
    """
    Returns dictionary with lowercase strings from a Page's Form's Fields
	"""
    fields = form_obj.fields
    keys = [field.key.text.lower() for field in fields]
    # Condition used because some field.keys do not have a corresponding field.value
    values = [field.value.text.lower() if field.value is not None else None for field in fields]
    return dict(zip(keys,values))

def get_expected_tokens(template_name='sysco.json'):
    # Fetch the required template type
    template_data = fetch_json(template_name)
    # Fetch the expected tokens and place in dictionary
    expected_tokens = template_data.get('expected_tokens')
    token_dict = {}
    for key in expected_tokens.keys():
        token_dict[int(key)] = expected_tokens[key]
    
    return token_dict