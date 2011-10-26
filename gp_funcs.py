def gp_add(a, b):
    return a + b

def gp_sub(a, b):
    return a - b

def gp_mul(a, b):
    return a * b

def gp_div(a, b):
    if b == 0:
        return a
    else:
        return a/b

def gp_igt(a, b, c, d):
    if a > b:
        return c
    else:
        return d