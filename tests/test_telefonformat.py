#!/usr/bin/env python

"""Tests for `telefonformat` package."""


import unittest

from telefonformat.formatter import format


class TestTelefonformat(unittest.TestCase):
    """Tests for `telefonformat` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_formatting(self):
        """Test area code Frankfurt"""
        numbers = (
            "+49 69 1234-567",
            "+49 (0 ) 69 1234-567",
            "0049 69 1234 567",
            "0 0 49 (0)69 1234567",
            "0 69/1234-567",
        )
        results = (
            (True, True,   "+49 (0)69 1234567"),
            (True, False,  "+49 69 1234567"),
            (False, False, "069 1234567"),
        )
        for number in numbers:
            for country_code, leading_zero, wanted_result in results:
                result, _ = format(number, country=country_code, leading_zero=leading_zero)
                self.assertEqual(result, wanted_result)

    def test_001_add_digits(self):
        """Test add digits, see https://is.gd/nNVq6Y """
        numbers = (
            # this is wrong, no leading zero here. we can't do this yet.
            ("+49 10 12 999", "+49 (0)1012 999"),

            # this is wrong, no leading zero here. we can't do this yet.
            # also no REMAINING digits - the 999 is also not happening
            ("+49 116 123 999", "+49 (0)116123 999"),

            # this is wrong, no leading zero here. we can't do this yet.
            # also no REMAINING digits - the 999 is also not happening
            ("+49 118 12 999", "+49 (0)11812 999"),

            # this is correct now. roughly.
            ("+49 19 123 999", "+49 (0)19123 999"),
            ("+49 31 1 999", "+49 (0)311 999"),
        )
        for check_me, wanted_result in numbers:
            result, _ = format(check_me)
            self.assertEqual(result, wanted_result)
