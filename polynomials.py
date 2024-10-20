class Monomial:
    @staticmethod
    def to_super(n):
        supers = list("⁰¹²³⁴⁵⁶⁷⁸⁹")
        chars = list(str(n))
        res = ""
        for char in chars:
            if char == "-":
                res += "⁻"
                continue
            res += supers[int(char)]
        return res

    @staticmethod
    def type_check(obj):
        if not isinstance(obj, (Monomial, Polynomial, int)):
            raise TypeError("Incorrect type")

    def __init__(self, koeff=1, *args):
        self.k = koeff
        self.vars = list(args)
        if not (any([var[1] for var in self.vars])):
            self.vars = [("", 0)].copy()
        self.base = set(self.vars)

    def copy(self):
        return Monomial(self.k, *self.vars)

    def fullw(self):
        elems = list()
        for var in self.vars:
            elems += [var[0]] * var[1]
        elems.sort()
        return "".join(elems)

    def __repr__(self):
        ret = ""
        if self.vars:
            self.vars.sort(key=lambda t: t[0])
        for var in self.vars:
            ret += var[0]
            if var[1] not in {0, 1}:
                ret += self.to_super(var[1])
        if not ret or self.k != 1:
            if self.k == -1:
                ret = "-" + ret
            else:
                ret = str(self.k) + ret
        return ret

    def __neg__(self):
        result = Monomial(-self.k, *self.vars)
        return result

    def __add__(self, other):
        self.type_check(other)
        if isinstance(other, int):
            return self + Monomial(other, ("", 0))
        if isinstance(other, Polynomial):
            return other + self
        if other.base == self.base:
            return Monomial(self.k + other.k, *self.vars)
        else:
            return Polynomial(self, other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        self.type_check(other)
        if isinstance(other, int):
            return self * Monomial(other, ("", 0))
        if isinstance(other, Polynomial):
            return other * self
        k_res = self.k * other.k
        res_vars = self.vars.copy()
        for var in other.vars:
            for own_var in self.vars:
                if var[0] == own_var[0]:
                    res_vars.remove(own_var)
                    new_power = var[1] + own_var[1]
                    if new_power != 0:
                        res_vars.append((own_var[0], new_power))
                    break
            else:
                res_vars.append(var)
        return Monomial(k_res, *res_vars)

    def __rmul__(self, other):
        return self * other


class Polynomial:
    def __init__(self, *mons):
        self.components = set(mons)

    def __repr__(self):
        if not self.components:
            return ""
        elems = list(self.components)
        elems.sort(key=lambda m: m.fullw())
        ret = str(elems.pop(0))
        for mon in elems:
            if mon.k > 0:
                ret += "+"
            ret += str(mon)
        return ret

    def copy(self):
        comps = [el.copy() for el in self.components]
        copied = Polynomial(*comps)
        return copied

    def __neg__(self):
        return Polynomial(*[Monomial(-m.k, *m.vars) for m in self.components])

    def __add_monomial(self, mon):
        result = self.copy()
        for elem in result.components:
            if elem.base == mon.base:
                result.components.remove(elem)
                k_res = elem.k + mon.k
                if k_res != 0:
                    result.components.add(Monomial(k_res, *elem.vars))
                return result
        else:
            result.components.add(mon)
            return result

    def __add__(self, other):
        result = self.copy()
        if isinstance(other, int):
            result = self + Monomial(other, ("", 0))
        elif isinstance(other, Monomial):
            result = result.__add_monomial(other)
        elif isinstance(other, Polynomial):
            for mon in other.components:
                result = result.__add_monomial(mon)
        return result

    def __radd__(self, other):
        return self + other

    def __mul_monomial(self, mon):
        result = Polynomial()
        for own_mon in self.components:
            result += own_mon * mon
        return result

    def __mul__(self, other):
        result = Polynomial()
        if isinstance(other, int):
            result = self * Monomial(other, ("", 0))
        elif isinstance(other, Monomial):
            result = self.__mul_monomial(other)
        elif isinstance(other, Polynomial):
            for other_mon in other.components:
                result += self.__mul_monomial(other_mon)
        return result

    def __rmul__(self, other):
        return self * other

    def __pow__(self, power, modulo=None):
        result = 1
        for i in range(power):
            result *= self
        return result
