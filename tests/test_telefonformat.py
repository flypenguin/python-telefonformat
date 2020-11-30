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
                result = format(number, country=country_code, leading_zero=leading_zero)
                self.assertEqual(result, wanted_result)

    def test_001_complex_numbers(self):
        """Test add digits, see https://is.gd/nNVq6Y """
        numbers = (
            ("+49 10 12 999", "+49 (0)1012 999"),
            ("+49 116 123 ", "+49 116123"),
            ("+49 118 12 ", "+49 11812"),
            ("110", "+49 110"),
            ("112", "+49 112"),

            # this is correct now. roughly.
            ("+49 19 123 999", "+49 (0)19123 999"),
            ("+49 31 1 999", "+49 (0)311 999"),
        )
        for check_me, wanted_result in numbers:
            result = format(check_me)
            self.assertEqual(result, wanted_result)

    def test_002_complex_numbers_no_country(self):
        """Test add digits, see https://is.gd/nNVq6Y """
        numbers = (
            ("+49 10 12 999", "01012 999"),
            ("+49 116 123 ", "116123"),
            ("+49 118 12 ", "11812"),
            ("110", "110"),
            ("112", "112"),

            # this is correct now. roughly.
            ("+49 19 123 999", "019123 999"),
            ("+49 31 1 999", "0311 999"),
        )
        for check_me, wanted_result in numbers:
            result = format(check_me, country=False)
            self.assertEqual(result, wanted_result)
