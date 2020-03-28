import pandas as pd
from utils import update_column_headers

class Orderitems():
    def __init__(self):
        self._Table = None
        self._TableDataFrame = None

    @property
    def Table(self, table_obj):
        self._Table = table_obj

    @property
    def TableDataFrame(self, df):
        self._TableDataFrame = df

    def create_TableDataFrame(self):
        df = pd.DataFrame([[cell.text for cell in row.cells] for row in self._Table.rows])
        return update_column_headers(df)

    def set_orderitem_values(self, table_obj):
        # Set Table object
        self._Table = table_obj
        # Set DataFrame
        self._TableDataFrame = self.create_TableDataFrame()

        _temp = self._TableDataFrame
        return _temp