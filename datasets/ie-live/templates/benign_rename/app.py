def calc_sum(nums):
    total = 0
    for n in nums:
        total += n
    return total


def sum_list(nums):
    # Bug: renamed wrapper still off-by-one
    return calc_sum(nums) + 1
