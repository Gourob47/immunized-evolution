def average(nums):
    # Bug: empty list divides by zero instead of returning None
    return sum(nums) / len(nums)
