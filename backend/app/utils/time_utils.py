from datetime import datetime

def utc_now():
    return datetime.now().strftime('%Y%m%d_%H%M%S')
