import re
import pandas as pd
import numpy as np
from preprocessor.constants import REGEX_MAP
from preprocessor.utils import update_column_headers, get_lineitem_expectations

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
        """
        Converts json from OCR to pandas DataFrame
        """
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
        """
        Helper function to strip leading and trailing whitespace
        """
        self._TableDataFrame[target_column] = self._TableDataFrame[target_column].apply(lambda x: x.strip())
    
    def strip_all_cols(self):
        """
        Stips all leading and trailing whitespace from each column in the DataFrame
        """
        for col in self._TableDataFrame.columns:
            self.strip_col(col)

    def lowercase_all_str_cols(self, expected_columns, expec_dtypes):
        """
        Used to convert string columns to lowercase.
        """
        for column in expected_columns:
            if expec_dtypes[column] == 'string':
                print(f'Converting {column} to lowercase.')
                self._TableDataFrame[column] = self._TableDataFrame[column].str.lower()

    def unbleed_single_column(self, target_column, num_expected_tokens = 1):
        """
        Warning: This assumes that Textract only accidentally misreads values to the left
        
        Used to unbleed columns (when a column's value gets read into column to the left)
        Moves stray tokens (words or numbers without spaces) into subsequent column if expected number of tokens is reached
        """
        # Print for debugging
        print(f"Running Unbleed: Column '{target_column} has expected number of tokens: {num_expected_tokens}.'")
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
                if original_string == '':
                    self._TableDataFrame.iloc[idx,col_idx+1] = extra_tokens[idx]    
                else:
                    self._TableDataFrame.iloc[idx,col_idx+1] = extra_tokens[idx] + ' ' + original_string
    
    def insert_missing_cols(self, expected_columns):
        """
        Takes list of expected columns (IN ORDER) and inserts into self._TableDataFrame if missing

        INPUTS
        expected_columns: list of expected columns in their intended order (from template)
        """
        inserted_columns = []
        for idx, column in enumerate(expected_columns):
            if column not in self._TableDataFrame.columns:
                print(f"Detected missing column: {column} | Inserting in position {idx}")
                # Inserts column with an empty value
                self._TableDataFrame.insert(idx, column, '')
                inserted_columns.append(column)
        return inserted_columns

    def pull_from_next_col(self, target_row_idx, target_col_idx, missing_tokens=1):
        """
        For a given row and column with known missing tokens, pulls token(s) from the subsequent cell in the DataFrame.
        Primarily used when 1) a column was not read by OCR service and 2) has a known number of tokens that the column must contain.
        If the unbleed on the previous column did not fill the missing value, this method pulls the first value out of the subsequent column
        
        Warning: prone to fail if 1) an inserted column follows a column with no definite expected tokens and 
            2) the OCR read any of the inserted column's values into the column with no definite expected tokens
        
        Future improvements can be made to make sure this method is only run on an inserted column following a column with known tokens
        """
        current_values = self._TableDataFrame.iloc[target_row_idx, target_col_idx].split()
        next_val_tokens = self._TableDataFrame.iloc[target_row_idx, target_col_idx+1].split()
        values_to_unbleed = next_val_tokens[:1]
        remaining_vals = next_val_tokens[1:]
        # Reassigning values to current cell and subsequent cell
        new_value = ' '.join(current_values+values_to_unbleed)
        self._TableDataFrame.iloc[target_row_idx, target_col_idx] = new_value
        self._TableDataFrame.iloc[target_row_idx, target_col_idx+1] = ' '.join(remaining_vals)

    def map_regex_groups_to_cols(self, column, expec_regex, drop_original=True):
        """
        Given an expectation on the regex of a column, map the groups to new columns, then optionally drop original column

        INPUTS
        column: column with regex expectation
        expec_regex: json containing regex str and resulting new columns
        """
        # Getting regex
        regex = expec_regex.get('regex')
        # Getting columns
        regex_cap_group_cols = expec_regex.get('capture_group_columns')
        print(f'Regex expectation for {column} detected. Creating new columns: {regex_cap_group_cols}.')
        # Extracting groups and creating new columns
        extracted_groups = self._TableDataFrame[column].str.extract(regex, expand=True)
        self._TableDataFrame[regex_cap_group_cols] = extracted_groups
        if drop_original==True:
            print(f'Dropped {column}.')
            self._TableDataFrame = self._TableDataFrame.drop(column, axis=1)

    def unbleed_columns(self, expected_columns, expec_tokens, expec_dtypes, inserted_columns, expec_regex):
        """
        Unbleed algorithm...
        1. Iterate through all expected columns after inserting missing columns
        2. If we have expected number of tokens for a column, run unbleed logic to re-distribute misread values

        INPUTS
        expected_columns: List of expected columns in their intende order (from template)
        expec_tokens: dictionary of columns and their expected number of tokens (from template)
        expec_dtypes: dictionary of columns and their expected data types (from template)
        inserted_columns: any columns that were initially not read by OCR and had to be inserted back into the DF
        expec_regex: regular expression for a column (if available) and its group -> column mapping

        RETURNS
        None - edits the self._TableDataFrame inplace 
        """
        # Iterate through columns for cleaning algorithm
        print(f"Running Unbleed for columns with an expected number of tokens...")
        for col_idx, column in enumerate(expected_columns):
            # Get expected num tokens, expected dtype, and regex
            num_expected_tokens = expec_tokens.get(column)
            expected_dtype = expec_dtypes.get(column)
            expected_regex = expec_regex.get(column)
            # If we have number of expected tokens...
            if num_expected_tokens is not None:
                # Handling reinserted columns with an expected number of tokens as a special case because these
                # ...will be empty if unbleed does not push values into them
                if column in inserted_columns:
                    print(f"Detected column with an expected number of columns that was not read by OCR")
                    print(f"\tColumn: {column} | Expected Tokens: {num_expected_tokens}")
                    # Checking if row has required tokens
                    # Setting a counter to check if values were pulled for debugging
                    values_pulled = 0
                    for row_idx in range(len(self._TableDataFrame)):
                        row_vals = self._TableDataFrame.iloc[row_idx,col_idx].split()
                        if len(row_vals) < num_expected_tokens:
                            values_pulled += 1
                            missing_tokens = num_expected_tokens-len(row_vals)
                            self.pull_from_next_col(target_row_idx=row_idx, target_col_idx=col_idx, missing_tokens=missing_tokens)
                        else:
                            pass
                    if values_pulled > 0:
                        print(f"Column '{column}' pulled from {values_pulled} rows because expected tokens were not met.")
                # If we have num_expected_tokens, run unbleed
                else:
                    self.unbleed_single_column(column, num_expected_tokens=num_expected_tokens)
            # Else if we have an expected regex, use it to create new columns
            elif expected_regex is not None:
                self.map_regex_groups_to_cols(column, expected_regex)
            # # If we do not have a number of expected tokens, accept
            else:
                pass

    def evaluate_expectations(self):
        """
        Iterates through expected columns, checks if columns were read, runs unbleed on columns, and converts to correct data type
        """
        # Get all expectations (num tokens, data types, and column order)
        expec_tokens, expec_dtypes, expected_columns, expec_regex = get_lineitem_expectations(template_name='sysco.json')
        # Insert all expected columns if missed
        inserted_columns = self.insert_missing_cols(expected_columns=expected_columns)
        # Lowercase all string columns
        self.lowercase_all_str_cols(expected_columns=expected_columns, expec_dtypes=expec_dtypes)

        # Run unbleed
        self.unbleed_columns(expected_columns=expected_columns, 
                            expec_tokens=expec_tokens,
                            expec_dtypes=expec_dtypes,
                            inserted_columns=inserted_columns,
                            expec_regex=expec_regex)

        # Perform regex parsing as a last resort
        self.regex_parsing(expec_dtypes)

    def regex_parsing(self, expected_dtypes):
        """
        Checks on all the constraints defined by a template and removes redundant values using
        regex
        """
        for column_name, dtype in expected_dtypes.items():
            if column_name not in self._TableDataFrame or dtype not in REGEX_MAP:
                continue
            self.regex_column_parsing(column_name, REGEX_MAP[dtype])


    def regex_column_parsing(self, column_name, regex):
        """
        Parses all the records in the columns and returns the first pattern match.
        If there is no match then it will return an empty string.
        """
        self._TableDataFrame[column_name] = self._TableDataFrame[column_name].apply(lambda x: re.findall(regex, x)[0])

    
    def remove_line_junk(self):
        """
        NOTE: Short term fix. Need to find a smarter solution for this later
        Used to remove known strings that may get misread into certain columns
        """
        line_junk = ['bottle deposit', 'recycling fee']


    def set_orderitems_dataframe(self, table_obj):
        # Set Table object
        self._Table = table_obj
        # Set DataFrame
        self._TableDataFrame = self.create_TableDataFrame()
        if len(self._TableDataFrame) == 0:
            print("Detected Empty Table.")
            return None
        # Strip all columns of whitespace
        self.strip_all_cols()
        # Remove non items (like categories or totals)
        self.remove_nonitem_rows()

        # Run expectations method - checks read DF against template expectations
        self.evaluate_expectations()



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

    



        