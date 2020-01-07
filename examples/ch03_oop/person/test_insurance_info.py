"""
Unit tests for Address class.
"""

from person.insurance_info import InsuranceInfo


def test_init_all_attributes() -> None:
    info: InsuranceInfo = InsuranceInfo('MVP', 'Premier Gold', '12340000', '432100', '783200')

    assert info.provider_name == 'MVP'
    assert info.plan_name == 'Premier Gold'
    assert info.account_id == '12340000'
    assert info.group_id == '432100'
    assert info.rx_bin_id == '783200'


def test_init_test_eq_true() -> None:
    info1: InsuranceInfo = InsuranceInfo('MVP', 'Premier Gold', '12340000', '432100', '783200')
    info2: InsuranceInfo = InsuranceInfo('MVP', 'Premier Gold', '12340000', '432100', '783200')

    assert info1 == info2


def test_init_test_ne_true() -> None:
    info1: InsuranceInfo = InsuranceInfo('MVP', 'Premier Gold', '12340000', '432100', '783200')
    info2: InsuranceInfo = InsuranceInfo('MVP', 'Premier Gold', '12340000', '432100', '783201')

    assert info1 != info2
