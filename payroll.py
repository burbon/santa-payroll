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


FM_N = [
    100, 20, 10, 5, 1,
    Decimal('0.25'), Decimal('0.1'), Decimal('0.05'), Decimal('0.01')
]


def fewest_money(amount):
    result = {}
    cnt = 0

    for n in FM_N:
        r = amount // n
        if r:
            result[n] = r
            cnt += r

        amount = amount % n

    return result, cnt


def payroll(elf, payday):
    ep = pay(elf, payday)
    js = JarSplit(ep)

    return ep, js
