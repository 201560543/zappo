from typing import List

class Order():
	def __init__(self):
		self._invoice_number = None
		self._customer = None
		self._vendor = None
		self._order_items = []

	def __str__(self):
		return f'{self._invoice_number}, number of items: {len(self._order_items)}'

	@property
	def invoice_number(self):
		return self._invoice_number

	@property
	def order_items(self):
		return [order_item for order_item in self._order_items]

	@property
	def vendor(self):
		return self._vendor

	def add_order_items(self, order_item):
		self._order_items.append(order_item)

	

