def sort_asc(nums):
    # Bug: sorts descending and mutates caller expectation via wrong order
    return sorted(nums, reverse=True)
