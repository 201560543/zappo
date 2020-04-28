from datetime import datetime

def converter(obj):
    """
    Used to convert an object into a json-serializable representation for api calls
    """
    if isinstance(obj, datetime):
        return obj.__str__()