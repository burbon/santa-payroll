from decimal import Decimal


class Payroll(object):
    def __init__(self, elf, payday):
        self.elf = elf
        self.payday = payday

        self.pay = self._pay()
        self.jar_split = JarSplit(self.pay)
        self.denomination = Denomination()

        self.denominate()

    def _pay(self):
        """
        Returns how much elf should be paid on a payday.
        Returns integer.
        """
        return round((self.elf.age(self.payday) * 52) / 12)

    def denominate(self):
        for jar in self.jar_split.jars.values():
            self.denomination.update(jar)

    def __str__(self):
        return "%s|%s|%s|%s" % (
            self.elf, self.pay, self.jar_split, self.denomination)


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
        self.jars = {}

        for jar_name, jar_tax in self.JARS.items():
            jar = jar_tax * self.amount
            self.__setattr__(jar_name, jar)
            self.jars[jar_name] = jar

    def __str__(self):
        return "{'charity': %s, 'retirement': %s, 'candy': %s}" % (
            self.charity, self.retirement, self.candy)


class Denomination(object):
    FM_N = [
        100, 20, 10, 5, 1,
        Decimal('0.25'), Decimal('0.1'), Decimal('0.05'), Decimal('0.01')
    ]

    def __init__(self):
        self.denomination = {}

    def update(self, amount):
        denomination = self.fewest_money(amount)
        self.update_from_denomination(denomination)

    def update_from_denomination(self, denomination):
        for k, v in denomination.items():
            if k not in self.denomination:
                self.denomination[k] = v
            else:
                self.denomination[k] += v

    @classmethod
    def fewest_money(cls, amount):
        result = {}

        for n in cls.FM_N:
            r = int(amount // n)
            if r:
                result[n] = r

            amount = amount % n

        return result

    def __str__(self):
        output = '{'
        for n, c in sorted(self.denomination.items(), reverse=True):
            output += "'%s': %s, " % (n, c)
        output = output[:-2]
        output += '}'
        return output


class Elf(object):
    def __init__(self, birthday, name=None, surname=None):
        self.name = name
        self.surname = surname
        self.birthday = birthday

    def age(self, date):
        diff = date.year - self.birthday.year
        if (date.month, date.day) < (self.birthday.month, self.birthday.day):
            diff -= 1

        return diff

    def __str__(self):
        return "%s %s" % (self.name, self.surname)
