"""
Unit tests for the Patient class.
"""

import copy
from datetime import datetime
from typing import List

from pytest import raises

from person.patient import Patient
from person.insurance_info import InsuranceInfo


ins_info: List[InsuranceInfo] = [
    InsuranceInfo(1, 'MVP', 'Premier Gold', '12340000', '432100', '783200'),
    InsuranceInfo(2, 'UHC', 'Premier Platinum', '54340000', '765400', '987600'),
]


def test_init() -> None:
    global ins_info
    patient: Patient = Patient("Curie", "Marie", "Skłodowska", ins_info)

    assert patient.full_name() == "Marie Skłodowska Curie"
    assert patient.insurance_info == ins_info
    assert patient.insurance_info is not ins_info


def test_add_insurance_info() -> None:
    global ins_info
    patient: Patient = Patient("Curie", "Marie", "Skłodowska")

    patient.add_ins_info(ins_info[0])

    assert patient.insurance_info == ins_info[:1]
    assert patient.insurance_info is not ins_info[:1]


def test_remove_insurance_info() -> None:
    global ins_info
    patient: Patient = Patient("Curie", "Marie", "Skłodowska", ins_info)

    patient.remove_ins_info('MVP', '12340000')

    assert patient.insurance_info == ins_info[1:]


def test_remove_all_insurance_info() -> None:
    global ins_info
    patient: Patient = Patient("Curie", "Marie", "Skłodowska", ins_info)

    patient.remove_ins_info('MVP', '12340000')
    patient.remove_ins_info('UHC', '54340000')

    assert patient.insurance_info == []


def test_eq_instances_equal() -> None:
    p1: Patient = Patient("Curie", "Marie", "Skłodowska", ins_info)
    p2: Patient = Patient("Curie", "Marie", "Skłodowska", ins_info)

    assert p1 == p2  # "==" calls p1.__eq__(p2) == p1


def test_eq_instances_not_equal() -> None:
    global ins_info
    p1: Patient = Patient("Curie", "Marie", None)
    p2: Patient = Patient("Curie", "Marie", "Skłodowska")

    assert p1 != p2  # "!=" calls p1.__ne__(p2)


def test_eq_diff_ins_info() -> None:
    p1: Patient = Patient("Curie", "Marie", "Skłodowska", ins_info[:1])
    p2: Patient = Patient("Curie", "Marie", "Skłodowska", ins_info[1:])

    assert p1 != p2  # "==" calls p1.__eq__(p2) == p1


def test_str() -> None:
    patient: Patient = Patient("Curie", "Marie", "Skłodowska")

    assert str(patient) == "Marie Skłodowska Curie"
