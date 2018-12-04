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
    def __init__(self, amount):
        self.amount = amount

        self.charity = Decimal('0.1') * self.amount
        self.retirement = Decimal('0.4') * self.amount
        self.candy = Decimal('0.5') * self.amount


def payroll(elf, payday):
    ep = pay(elf, payday)
    js = JarSplit(ep)

    return ep, js
