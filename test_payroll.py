from datetime import date
from decimal import Decimal

from payroll import Payroll, Paycheck, Denomination, Elf

import pytest


@pytest.fixture
def elf():
    return Elf(date.fromisoformat('2007-01-01'), 'Alabaster', 'Snow')


@pytest.fixture
def elf2():
    return Elf(date.fromisoformat('1907-01-01'), 'Foo', 'Bar')


@pytest.fixture
def payday():
    return date.fromisoformat('2019-01-01')


@pytest.fixture
def pay(payday, elf):
    return Payroll(payday).pay(elf)


@pytest.fixture
def paycheck(elf, pay):
    """
    12 year old elf paycheck
    """
    return Paycheck(elf, pay, Payroll.JARS)


def test_payroll_pay(pay):
    # (12 * 52) / 12 = 52
    assert pay == 52


def test_paycheck(paycheck, pay):
    assert paycheck.pay == pay

    assert paycheck.charity == Decimal('5.2')
    assert paycheck.retirement == Decimal('20.8')
    assert paycheck.candy == Decimal('26')


def test_paycheck_denomination(paycheck):
    # 5.2
    assert Denomination.fewest_money(paycheck.charity) == {
        5: 1, D('0.1'): 2}
    # 20.8
    assert Denomination.fewest_money(paycheck.retirement) == {
        20: 1, D('0.25'): 3, D('0.05'): 1}
    # 26
    assert Denomination.fewest_money(paycheck.candy) == {
        20: 1, 5: 1, 1: 1}

    assert paycheck.denomination.denomination == {
        20: 2, 5: 2, 1: 1, D('0.25'): 3, D('0.1'): 2, D('0.05'): 1
    }


def test_payroll_output(payday, elf, elf2):
    p = Payroll(payday, [elf, elf2])
    expected = 'Alabaster Snow|52|' \
        "{'charity': 5.2, 'retirement': 20.8, 'candy': 26.0}|" \
        "{'20': 2, '5': 2, '1': 1, '0.25': 3, '0.1': 2, '0.05': 1}\n" \
        "Foo Bar|485|" \
        "{'charity': 48.5, 'retirement': 194.0, 'candy': 242.5}|" \
        "{'100': 3, '20': 8, '10': 1, '5': 1, '1': 9, '0.25': 4}\n" \
        "\nTotal denomination: " \
        "{'100': 3, '20': 10, '10': 1, '5': 3, '1': 10, " \
        "'0.25': 7, '0.1': 2, '0.05': 1}"

    assert str(p) == expected


def test_paycheck_output(paycheck):
    assert str(paycheck.elf) == 'Alabaster Snow'
    assert str(paycheck.pay) == '52'
    assert str(paycheck.jars) == \
        "{'charity': 5.2, 'retirement': 20.8, 'candy': 26.0}"
    assert str(paycheck.denomination) == \
        "{'20': 2, '5': 2, '1': 1, '0.25': 3, '0.1': 2, '0.05': 1}"

    assert str(paycheck) == '%s|%s|%s|%s' % (
        paycheck.elf, paycheck.pay, paycheck.jars, paycheck.denomination)


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
    assert Payroll(payday).pay(elf) == 4


def test_pay_fraction_round_up():
    elf = Elf(date.fromisoformat('2007-01-01'))
    payday = date.fromisoformat('2009-01-01')
    # (2 * 52) / 12 = 8.66
    assert Payroll(payday).pay(elf) == 9


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


def test_paycheck_whole(elf):
    paycheck = Paycheck(elf, 100, Payroll.JARS)
    assert paycheck.charity == 10
    assert paycheck.retirement == 40
    assert paycheck.candy == 50


def test_paycheck_fraction(elf):
    paycheck = Paycheck(elf, 3, Payroll.JARS)
    assert paycheck.charity == Decimal('0.3')
    assert paycheck.retirement == Decimal('1.2')
    assert paycheck.candy == Decimal('1.5')


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
    p = Payroll(payday(), [elf(), elf2()])
    print(p)
