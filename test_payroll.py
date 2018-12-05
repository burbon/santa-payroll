from datetime import date
from decimal import Decimal

from payroll import Payroll, JarSplit, Denomination, Elf

import pytest


@pytest.fixture
def elf():
    return Elf(date.fromisoformat('2007-01-01'), 'Alabaster', 'Snow')


@pytest.fixture
def payday():
    return date.fromisoformat('2019-01-01')


@pytest.fixture
def payroll(elf, payday):
    """
    12 year old elf payroll
    """
    return Payroll(elf, payday)


def test_payroll_pay(payroll):
    # (12 * 52) / 12 = 52
    assert payroll.pay == 52


def test_payroll_jar_split(payroll):
    assert payroll.pay == payroll.jar_split.amount

    assert payroll.jar_split.charity == Decimal('5.2')
    assert payroll.jar_split.retirement == Decimal('20.8')
    assert payroll.jar_split.candy == Decimal('26')


def test_payroll_denomination(payroll):
    # 5.2
    assert Denomination.fewest_money(payroll.jar_split.charity) == {
        5: 1, D('0.1'): 2}
    # 20.8
    assert Denomination.fewest_money(payroll.jar_split.retirement) == {
        20: 1, D('0.25'): 3, D('0.05'): 1}
    # 26
    assert Denomination.fewest_money(payroll.jar_split.candy) == {
        20: 1, 5: 1, 1: 1}

    assert payroll.denomination.denomination == {
        20: 2, 5: 2, 1: 1, D('0.25'): 3, D('0.1'): 2, D('0.05'): 1
    }


def test_payroll_output(payroll):
    assert str(payroll.elf) == 'Alabaster Snow'
    assert str(payroll.pay) == '52'
    assert str(payroll.jar_split) == \
        "{'charity': 5.2, 'retirement': 20.8, 'candy': 26.0}"
    assert str(payroll.denomination) == \
        "{'20': 2, '5': 2, '1': 1, '0.25': 3, '0.1': 2, '0.05': 1}"

    assert str(payroll) == '%s|%s|%s|%s' % (
        payroll.elf, payroll.pay, payroll.jar_split, payroll.denomination)


def test_elf_age_had_birthday_that_year():
    elf = Elf(date.fromisoformat('2007-01-02'))
    on_date = date.fromisoformat('2019-01-02')
    assert elf.age(on_date) == 12


def test_elf_age_no_birthday_that_year_yet():
    elf = Elf(date.fromisoformat('2007-01-02'))
    on_date = date.fromisoformat('2019-01-01')
    assert elf.age(on_date) == 11


def test_pay_fraction_round_down():
    elf = Elf(date.fromisoformat('2007-01-01'))
    payday = date.fromisoformat('2008-01-01')
    # (1 * 52) / 12 = 4.33
    assert Payroll(elf, payday).pay == 4


def test_pay_fraction_round_up():
    elf = Elf(date.fromisoformat('2007-01-01'))
    payday = date.fromisoformat('2009-01-01')
    # (2 * 52) / 12 = 8.66
    assert Payroll(elf, payday).pay == 9


D = Decimal


@pytest.mark.parametrize("test_amount,expected", [
    (1, {1: 1}),
    (2, {1: 2}),
    (4, {1: 4}),
    (5, {5: 1}),
    (6, {5: 1, 1: 1}),
    (136, {100: 1, 20: 1, 10: 1, 5: 1, 1: 1}),
    (272, {100: 2, 20: 3, 10: 1, 1: 2}),

    (D('0.01'), {D('0.01'): 1}),
    (D('0.02'), {D('0.01'): 2}),
    (D('0.04'), {D('0.01'): 4}),
    (D('0.05'), {D('0.05'): 1}),
    (D('0.06'), {D('0.05'): 1, D('0.01'): 1}),
    (D('0.66'), {D('0.25'): 2, D('0.1'): 1, D('0.05'): 1, D('0.01'): 1}),

    (D('272.66'), {
        100: 2, 20: 3, 10: 1, 1: 2,
        D('0.25'): 2, D('0.1'): 1, D('0.05'): 1, D('0.01'): 1}),
])
def test_fewest_money(test_amount, expected):
    assert Denomination.fewest_money(test_amount) == expected


def test_jar_split_whole():
    jar_split = JarSplit(100)
    assert jar_split.charity == 10
    assert jar_split.retirement == 40
    assert jar_split.candy == 50


def test_jar_split_fraction():
    jar_split = JarSplit(3)
    assert jar_split.charity == Decimal('0.3')
    assert jar_split.retirement == Decimal('1.2')
    assert jar_split.candy == Decimal('1.5')


@pytest.mark.parametrize("total,jar_denomination,expected", [
    ({}, {1: 1}, {1: 1}),
    ({1: 1}, {1: 1}, {1: 2}),
    ({1: 2}, {1: 2}, {1: 4}),
    ({1: 4}, {2: 2}, {1: 4, 2: 2}),
    ({1: 4, 2: 2}, {2: 2, 5: 1}, {1: 4, 2: 4, 5: 1}),
])
def test_denomination_update(total, jar_denomination, expected):
    denomination = Denomination()
    denomination.denomination = total
    denomination.update_from_denomination(jar_denomination)
    assert denomination.denomination == expected


if __name__ == "__main__":
    e = elf()
    d = payday()
    p = payroll(e, d)
    print(p)
