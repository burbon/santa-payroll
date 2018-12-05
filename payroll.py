from decimal import Decimal


class Payroll(object):
    JARS = {
        'charity': Decimal('0.1'),
        'retirement': Decimal('0.4'),
        'candy': Decimal('0.5'),
    }

    def __init__(self, payday, elfs=None):
        self.payday = payday
        self.elfs = elfs
        if not self.elfs:
            self.elfs = []

        self.denomination = Denomination()

    def __str__(self):
        output = ''
        for elf in self.elfs:
            paycheck = self.paycheck(elf)
            output += "%s\n" % paycheck
        output += "\n"

        output += "Total denomination: %s" % self.denomination

        return output

    def paycheck(self, elf):
        pay = self.pay(elf)
        paycheck = Paycheck(elf, pay, self.JARS)

        self.denomination.update_from_denomination(paycheck.denomination)

        return paycheck

    def pay(self, elf):
        """
        Returns how much elf should be paid on a payday.
        Returns integer.
        """
        return round((elf.age(self.payday) * 52) / 12)


class Paycheck(object):
    def __init__(self, elf, pay, jars):
        self.elf = elf
        self.pay = pay
        self.jars_def = jars

        self.jars = Jars()
        self.denomination = Denomination()

        self.build_jars()

    def __str__(self):
        return "%s|%s|%s|%s" % (
            self.elf, self.pay, self.jars, self.denomination)

    def build_jars(self):
        for jar_name, jar_tax in self.jars_def.items():
            money = jar_tax * self.pay
            self.__setattr__(jar_name, money)
            self.jars[jar_name] = money
            self.denomination.update_from_money(money)


class Jars(dict):
    def __str__(self):
        return "{'charity': %s, 'retirement': %s, 'candy': %s}" % (
            self['charity'], self['retirement'], self['candy'])


class Denomination(dict):
    FM_N = [
        100, 20, 10, 5, 1,
        Decimal('0.25'), Decimal('0.1'), Decimal('0.05'), Decimal('0.01')
    ]

    def __str__(self):
        output = '{'
        for n, c in sorted(self.items(), reverse=True):
            output += "'%s': %s, " % (n, c)
        output = output[:-2]
        output += '}'
        return output

    def update_from_money(self, amount):
        denomination = self.fewest_money(amount)
        self.update_from_denomination(denomination)

    def update_from_denomination(self, denomination):
        for k, v in denomination.items():
            if k not in self:
                self[k] = v
            else:
                self[k] += v

    @classmethod
    def fewest_money(cls, amount):
        result = {}

        for n in cls.FM_N:
            r = int(amount // n)
            if r:
                result[n] = r

            amount = amount % n

        return result


class Elf(object):
    def __init__(self, birthday, name=None, surname=None):
        self.name = name
        self.surname = surname
        self.birthday = birthday

    def __str__(self):
        return "%s %s" % (self.name, self.surname)

    def age(self, date):
        diff = date.year - self.birthday.year
        if (date.month, date.day) < (self.birthday.month, self.birthday.day):
            diff -= 1

        return diff
