from web import db

class OrderItem(db.Model):
    """
    Used to store item-level information
    """
    item_number = db.Column(db.String(32))
    order_quantity = db.Column(db.String(32))
    shipped_quantity = db.Column(db.String(32))
    unit = db.Column(db.String(32))
    size = db.Column(db.String(32))
    brand = db.Column(db.String(32))
    description = db.Column(db.String(32))
    weight = db.Column(db.String(32))
    price = db.Column(db.String(32))
    total_price = db.Column(db.String(32))
    
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