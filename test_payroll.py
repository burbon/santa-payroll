from datetime import date

from payroll import payroll, Elf


def test_elf_age_had_birthday_that_year():
    elf = Elf(date.fromisoformat('2007-01-02'))
    on_date = date.fromisoformat('2019-01-02')
    assert elf.age(on_date) == 12


def test_elf_age_no_birthday_that_year_yet():
    elf = Elf(date.fromisoformat('2007-01-02'))
    on_date = date.fromisoformat('2019-01-01')
    assert elf.age(on_date) == 11


def test_payroll_integer():
    elf = Elf(date.fromisoformat('2007-01-01'))
    payday = date.fromisoformat('2019-01-01')
    # (12 * 52) / 12 = 52
    assert payroll(elf, payday) == 52


def test_payroll_round_down():
    elf = Elf(date.fromisoformat('2007-01-01'))
    payday = date.fromisoformat('2008-01-01')
    # (1 * 52) / 12 = 4.33
    assert payroll(elf, payday) == 4


def test_payroll_round_up():
    elf = Elf(date.fromisoformat('2007-01-01'))
    payday = date.fromisoformat('2009-01-01')
    # (2 * 52) / 12 = 8.66
    assert payroll(elf, payday) == 9
