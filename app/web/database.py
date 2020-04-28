from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

db = SQLAlchemy()

def prepare_automap_base(db):
    """
    Used to generate a Base object with classes/models automatically mapped to database.
    To access a particular model, use the following syntax (example for Address Model)...
        Base = prepare_automap_base(db)
        Address = Base.classes.address
        for address in db.session.query(Address).all():
            print(address.id)
    
    Note that you must access each attribute of these automap classes individually. 
    Using the automap base makes it easier to create new objects because it can be treated as a class.

    INPUT: ORM object
    RETURNS: Base object
    """
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)
    return Base

def create_autogen_table(db, tablename):
    """
    Used to generate a Table object with models automatically mapped to database.
    To access a particular model, use the following syntax (example for Address Model)...
        Address = create_autogen_table(db,'address')
        results = Address.query.all()
        print(results)
    
    Note that using Tables makes it easier to fetch results because you don't need to access attributes individually.

    INPUT: ORM object
    RETURNS: Table object
    """
    return db.Table(tablename, db.metadata, autoload=True, autoload_with=db.engine)