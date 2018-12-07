import argparse
import csv
from datetime import date
from decimal import Decimal
from functools import reduce


class Payroll(object):
    JARS = {
        'charity': Decimal('0.1'),
        'retirement': Decimal('0.4'),
        'candy': Decimal('0.5'),
    }

    def __init__(self, payday, elves=None):
        self.payday = payday
        self.elves = elves
        if not self.elves:
            self.elves = []

        self.change = Change()
        self.report = []

    def __str__(self):
        output = ''
        for paycheck in self.report:
            output += "%s\n" % paycheck
        output += "\n"

        output += "Total change: %s" % self.change

        return output

    def run(self):
        for elf in self.elves:
            self.report.append(self.paycheck(elf))

    def add_elf(self, elf):
        self.elves.append(elf)

    def paycheck(self, elf):
        pay = self.pay(elf)
        paycheck = Paycheck(elf, pay, self.JARS)

        self.change.update_from_change(paycheck.change)

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
        self.change = Change()

        self.build_jars()

    def __str__(self):
        return "%s|%s|%s" % (
            self.elf, self.pay, self.jars)

    def build_jars(self):
        for jar_name, jar_tax in self.jars_def.items():
            money = jar_tax * self.pay
            self.__setattr__(jar_name, money)
            self.jars[jar_name] = money
            self.change.update_from_money(money)


class Jars(dict):
    def __str__(self):
        return "{'charity': %s, 'retirement': %s, 'candy': %s}" % (
            self['charity'], self['retirement'], self['candy'])


class Change(dict):
    DENOMINATION = [
        100, 20, 10, 5, 1,
        Decimal('0.25'), Decimal('0.1'), Decimal('0.05'), Decimal('0.01')
    ]

    def __str__(self):
        if not self.items():
            return "{}"

        output = reduce(
            lambda x, y: ', '.join([x, y]),
            map(
                lambda i: "%s: %s" % (i[0], i[1]),
                sorted(self.items(), reverse=True)),
        )
        return "{%s}" % output

    def update_from_money(self, amount):
        change = self.make(amount)
        self.update_from_change(change)

    def update_from_change(self, change):
        for k, v in change.items():
            if k not in self:
                self[k] = v
            else:
                self[k] += v

    @classmethod
    def make(cls, amount):
        result = {}

        for n in cls.DENOMINATION:
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
        return "%s" % self.name

    def age(self, date):
        diff = date.year - self.birthday.year
        if (date.month, date.day) < (self.birthday.month, self.birthday.day):
            diff -= 1

        return diff


def argparser():
    parser = argparse.ArgumentParser(
        description='Santa\'s Payroll'
    )

    parser.add_argument('elves', type=open)
    parser.add_argument('-d', type=date.fromisoformat,
                        dest='payday', default=date.today())

    return parser


def main():
    parser = argparser()
    args = parser.parse_args()
    payroll = Payroll(args.payday)
    with args.elves as fd:
        csv_reader = csv.reader(fd, delimiter=',')
        for row in csv_reader:
            elf = Elf(date.fromisoformat(row[1]), row[0])
            payroll.add_elf(elf)

    payroll.run()
    print(payroll)


if __name__ == "__main__":
    main()
