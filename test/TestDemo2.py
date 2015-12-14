def make_adder(addend):
    def adder(augend):
        return augend + addend
    return adder

p = make_adder(23)
q = make_adder(44)

print p(100)
print q(100)

