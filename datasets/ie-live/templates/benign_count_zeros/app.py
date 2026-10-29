def count_zeros(nums):
    # Bug: crashes on empty; treats None as zero
    if not nums:
        raise ValueError('empty')
    return sum(1 for n in nums if not n)
