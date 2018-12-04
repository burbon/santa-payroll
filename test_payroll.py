from datetime import date
from decimal import Decimal

from payroll import pay, Elf, JarSplit, payroll, fewest_money

import pytest


def test_elf_age_had_birthday_that_year():
    elf = Elf(date.fromisoformat('2007-01-02'))
    on_date = date.fromisoformat('2019-01-02')
    assert elf.age(on_date) == 12


def test_elf_age_no_birthday_that_year_yet():
    elf = Elf(date.fromisoformat('2007-01-02'))
    on_date = date.fromisoformat('2019-01-01')
    assert elf.age(on_date) == 11


def test_pay_whole():
    elf = Elf(date.fromisoformat('2007-01-01'))
    payday = date.fromisoformat('2019-01-01')
    # (12 * 52) / 12 = 52
    assert pay(elf, payday) == 52


def test_pay_fraction_round_down():
    elf = Elf(date.fromisoformat('2007-01-01'))
    payday = date.fromisoformat('2008-01-01')
    # (1 * 52) / 12 = 4.33
    assert pay(elf, payday) == 4


def test_pay_fraction_round_up():
    elf = Elf(date.fromisoformat('2007-01-01'))
    payday = date.fromisoformat('2009-01-01')
    # (2 * 52) / 12 = 8.66
    assert pay(elf, payday) == 9


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
    assert fewest_money(test_amount) == expected


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
def test_jar_split_update_denomination(total, jar_denomination, expected):
    jar_split = JarSplit(0)
    jar_split.denomination = total
    jar_split._JarSplit__update_denomination(jar_denomination)
    assert jar_split.denomination == expected


def test_jar_split_denomination():
    jar_split = JarSplit(103)

    assert jar_split.charity == Decimal('10.3')
    assert fewest_money(jar_split.charity) == {
        10: 1, D('0.25'): 1, D('0.05'): 1}

    assert jar_split.retirement == Decimal('41.2')
    assert fewest_money(jar_split.retirement) == {
        20: 2, 1: 1, D('0.1'): 2}

    assert jar_split.candy == Decimal('51.5')
    assert fewest_money(jar_split.candy) == {
        20: 2, 10: 1, 1: 1, D('0.25'): 2}

    assert jar_split.denomination == {
        20: 4, 10: 2, 1: 2, D('0.25'): 3, D('0.1'): 2, D('0.05'): 1
    }


def test_payroll():
    elf = Elf(date.fromisoformat('2007-01-02'))
    payday = date.fromisoformat('2019-01-02')

    elf_pay, jar_split = payroll(elf, payday)
    assert elf_pay == jar_split.amount
