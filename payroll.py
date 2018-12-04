from decimal import Decimal


class Elf(object):
    def __init__(self, birthday):
        self.birthday = birthday

    def age(self, date):
        diff = date.year - self.birthday.year
        if (date.month, date.day) < (self.birthday.month, self.birthday.day):
            diff -= 1

        return diff


def pay(elf, payday):
    """
    Returns how much elf should be paid on a payday.
    Returns integer.
    """
    return round((elf.age(payday) * 52) / 12)


class JarSplit(object):
    """
    Represents 3 jars split
    """
    JARS = {
        'charity': Decimal('0.1'),
        'retirement': Decimal('0.4'),
        'candy': Decimal('0.5'),
    }

    def __init__(self, amount):
        self.amount = amount
        self.denomination = {}

        for jar_name, jar_tax in self.JARS.items():
            jar = jar_tax * self.amount
            self.__setattr__(jar_name, jar)

            jar_denomination = fewest_money(jar)
            self.__update_denomination(jar_denomination)

    def __update_denomination(self, denomination):
        for k, v in denomination.items():
            if k not in self.denomination:
                self.denomination[k] = v
            else:
                self.denomination[k] += v


FM_N = [
    100, 20, 10, 5, 1,
    Decimal('0.25'), Decimal('0.1'), Decimal('0.05'), Decimal('0.01')
]


def fewest_money(amount):
    result = {}

    for n in FM_N:
        r = amount // n
        if r:
            result[n] = r

        amount = amount % n

    return result


def payroll(elf, payday):
    ep = pay(elf, payday)
    js = JarSplit(ep)

    return ep, js
