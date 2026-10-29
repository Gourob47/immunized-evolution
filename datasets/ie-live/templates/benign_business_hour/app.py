def is_business_hour(hour):
    # Bug: off-by-one, treats 8-16 as business hours
    return 8 <= hour <= 16
