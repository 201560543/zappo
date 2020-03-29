import pandas as pd
import numpy as np
from utils import update_column_headers

class Orderitems():
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
        self._TableDataFrame[target_column] = self._TableDataFrame[target_column].apply(lambda x: x.strip())
    
    def strip_all_cols(self):
        for col in self._TableDataFrame.columns:
            self.strip_col(col)
    
    # NOTE: needs to be completed
    # def unbleed_columns(self):
    #     """
    #     Adjusts/redistributes strings read into incorrect columns by Textract
    #     """
    #     self.unbleed_item_number()
    
    def unbleed_column(self, target_column, num_expected_tokens = 1):
        """
        Moves stray tokens (words or numbers without spaces) into subsequent column if expected number of tokens is reached
        """
        split_rows = self._TableDataFrame[target_column].apply(lambda x: x.split())
        expected_tokens, extra_tokens = [], []
        for row in split_rows:
            # Appends a space after the value
            expected_tokens.append(row[0]+ ' ')
            if len(row) > num_expected_tokens:
                extra_tokens.append(row[1:])
            else:
                extra_tokens.append('')
        
        self.reinsert_unbled_cols(target_column, expected_tokens, extra_tokens)
    
    def reinsert_unbled_cols(self, target_column, expected_tokens, extra_tokens):
        """
        Used to unbleed columns (when a column's value gets read into column to the left)
        Reinserts expected tokens into target column and extra tokens into the next column
        """
        # Getting column index
        col_idx = np.where(self._TableDataFrame.columns == target_column)[0][0]

        self._TableDataFrame[target_column] = expected_tokens
        # Insert extra values only
        for idx, token in enumerate(extra_tokens):
            if token == '':
                break
            self._TableDataFrame.iloc[idx,col_idx+1] = extra_tokens[idx]
        
        # NOTE: TBC - consider adding expected number of tokens to template file
    
    
    def set_orderitems_dataframe(self, table_obj):
            # Set Table object
            self._Table = table_obj
            # Set DataFrame
            self._TableDataFrame = self.create_TableDataFrame()
            # Strip all columns of whitespace
            self.strip_all_cols()
            # Remove non items (like categories or totals)
            self.remove_nonitem_rows()

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

    



        