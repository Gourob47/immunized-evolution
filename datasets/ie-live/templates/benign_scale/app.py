def scale_scores(nums, factor):
    # Bug: adds factor instead of multiplying
    return [n + factor for n in nums]
