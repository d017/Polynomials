from polynomials import *

m1 = Monomial(1, ("x", 1))
m2 = Monomial(1, ("y", 1))
m3 = Monomial(1, ("z", 1))

p1 = Polynomial(m1, -m2*m3)
p2 = Polynomial(m2, m3)

print(f"({m1}+{m2}+{m3})^2 = {(m1 + m2 + m3) ** 2}")
print(f"({m1}-{m2})^3 = {(m1 - m2) ** 3}")
print(f"({p1})({p2}) = {p1 * p2}")
