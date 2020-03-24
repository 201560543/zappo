from typing import List

class Order():
	def __init__(self):
		self.invoice_number = None
		self.customer = None
		self.vendor = None
		self.order_items = []

	def __str__(self):
		return f'{self.invoice_number}, number of items: {len(self.order_items)}'

	@property
	def invoice_number(self):
		return self.invoice_number


	@property
	def order_items(self):
		return [order_item for order_item in self.order_items]


	@property
	def vendor(self):
		return self.vendor


	def add_order_items(self, order_item:):
		self.order_items.append(order_item)

