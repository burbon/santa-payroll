class Elf(object):
    def __init__(self, birthday):
        self.birthday = birthday

    def age(self, date):
        diff = date.year - self.birthday.year
        if (date.month, date.day) < (self.birthday.month, self.birthday.day):
            diff -= 1

        return diff


def payroll(elf, payday):
    return round((elf.age(payday) * 52) / 12)
