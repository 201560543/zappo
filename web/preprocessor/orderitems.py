import pandas as pd
import numpy as np
from utils import update_column_headers, get_expected_tokens

class OrderitemsDF():
    """
    Used to store extracted information in tabular format
    """
    def __init__(self):
        self._Table = None
        self._TableDataFrame = None

    @property
    def Table(self, table_obj):
        return self._Table

    @property
    def TableDataFrame(self):
        return self._TableDataFrame

    def create_TableDataFrame(self):
        df = pd.DataFrame([[cell.text for cell in row.cells] for row in self._Table.rows])
        return update_column_headers(df)
    
    def remove_nonitem_rows(self):
        """
        Removes extracted rows that are not order items (totals, categories, etc.)
        Assumes anything without an item_number is not an item
        """
        df = self._TableDataFrame
        self._TableDataFrame = df[df['item_number'] != '']
    
    def strip_col(self, target_column):
        print(self._TableDataFrame[target_column])
        self._TableDataFrame[target_column] = self._TableDataFrame[target_column].apply(lambda x: x.strip())
    
    def strip_all_cols(self):
        for col in self._TableDataFrame.columns:
            self.strip_col(col)
    
    def unbleed_columns(self):
        """
        Adjusts/redistributes strings read into incorrect columns by Textract
        """
        token_dict = get_expected_tokens(template_name='sysco.json')
        for num_expected_tokens in token_dict.keys():
            cols = token_dict[num_expected_tokens]
            for col in cols:
                self.unbleed_single_column(target_column=col, num_expected_tokens=num_expected_tokens)
    
    # Warning: This assumes that Textract only accidentally misreads values to the left
    def unbleed_single_column(self, target_column, num_expected_tokens = 1):
        """
        Used to unbleed columns (when a column's value gets read into column to the left)
        Moves stray tokens (words or numbers without spaces) into subsequent column if expected number of tokens is reached
        """
        split_rows = self._TableDataFrame[target_column].apply(lambda x: x.split())
        expected_tokens, extra_tokens = [], []
        for row in split_rows:
            # Appends a space after the value
            expected_tok_string = ' '.join(row[:num_expected_tokens])
            expected_tokens.append(expected_tok_string)
            if len(row) > num_expected_tokens:
                extra_tok_string = ' '.join(row[num_expected_tokens:])
                extra_tokens.append(extra_tok_string)
            else:
                extra_tokens.append('')
        
        self.reinsert_unbled_cols(target_column, expected_tokens, extra_tokens)
    
    def reinsert_unbled_cols(self, target_column, expected_tokens, extra_tokens):
        """
        Used to unbleed columns (when a column's value gets read into column to the left)
        Reinserts expected tokens into target column and extra tokens into the subsequent column
        """
        # Getting column index
        col_idx = np.where(self._TableDataFrame.columns == target_column)[0][0]
        # Insert expected tokens to the target
        self._TableDataFrame[target_column] = expected_tokens
        # Insert extra values only to the next column
        for idx, token in enumerate(extra_tokens):
            if token != '':
                # Appends the original extracted string onto the extra tokens
                original_string = self._TableDataFrame.iloc[idx,col_idx+1]
                self._TableDataFrame.iloc[idx,col_idx+1] = extra_tokens[idx] + ' ' + original_string
    
    def pre_validate_column(self, target_column, expected_tokens, token_type):
        """
        Checks whether a column is ready to be converted to its correct data type.
        e.g. If item_number (to be converted to int) has 1 token, and that token is all numeric, it should pass this check
        """
        # return here: add expected data types to template

    
    def set_orderitems_dataframe(self, table_obj):
        # Set Table object
        self._Table = table_obj
        # Set DataFrame
        self._TableDataFrame = self.create_TableDataFrame()
        # Strip all columns of whitespace
        self.strip_all_cols()
        # Remove non items (like categories or totals)
        self.remove_nonitem_rows()
        # Unbleed columns
        self.unbleed_columns()
    
    def convert_DF_to_Orderitem_objs(self):
        for idx in range(len(self._TableDataFrame)):
            orderitem = Orderitem()
            row_dict = self._TableDataFrame.iloc[idx,:].to_dict()
            orderitem.set_attributes(row_dict)

            # For debugging
            # print(orderitem)

        print(self._TableDataFrame)

class Orderitem():
    """
    Used to store item-level information
    """
    def __init__(self):
        self.item_number = None
        self.order_quantity = None
        self.shipped_quantity = None
        self.unit = None
        self.size = None
        self.brand = None
        self.description = None
        self.weight = None
        self.price = None
        self.total_price = None
    
    def __repr__(self):
        return f'''{[
            self.item_number,
            self.order_quantity,
            self.shipped_quantity,
            self.unit,
            self.size,
            self.brand,
            self.description,
            self.weight,
            self.price,
            self.total_price
            ]}'''
    
    def set_attributes(self, data):
        for key, val in data.items():
            if hasattr(self, key):
                setattr(self, f'{key}', val)

    



        