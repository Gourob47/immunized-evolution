def unit_price(total, qty):
    # Bug: integer division and no zero guard
    return total // qty if qty else 0
