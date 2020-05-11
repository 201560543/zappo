from flask import Blueprint

api = Blueprint('api', __name__)
account = Blueprint('account', __name__)
address = Blueprint('address', __name__)
organization = Blueprint('organization', __name__)
supplier = Blueprint('supplier', __name__)
person = Blueprint('person', __name__)
person_account = Blueprint('person_account', __name__)
restaurant = Blueprint('restaurant', __name__)