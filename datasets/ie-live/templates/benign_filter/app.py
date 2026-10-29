def filter_positive(nums):
    # Bug: keeps zeros and negatives that are not < -10
    return [n for n in nums if n >= 0]
