#!/usr/bin/env python

"""Main module."""

import re

from .vorwahlen import vorwahlen


def split(number):
    """Returns (prefix, area, number)"""

    nr_ = re.sub("[^0-9+]", "", number)

    if nr_.startswith("+49"):
        nr_ = nr_[3:]
    elif nr_.startswith("00"):
        nr_ = nr_[4:]

    # it COULD have been: "+49(0)221...."
    if nr_.startswith("0"):
        nr_ = nr_[1:]

    phone_number = nr_

    for cnt in range(5, 1, -1):
        area_code = nr_[:cnt]
        if nr_[:cnt] in vorwahlen:
            info = vorwahlen[area_code]
            if info.add_digits:
                area_code = nr_[:(cnt + info.add_digits)]
            phone_number = nr_[(cnt+info.add_digits):]

            if info.is_final:
                if phone_number:
                    raise ValueError("Surplus digits: " + phone_number)
                else:
                    phone_number = area_code
                    area_code = ""
            break
    else:
        return None

    return (
        "0" if not info.is_final else "",
        area_code,
        phone_number,
        info.info,
    )


def format_split(info_tuple, country=True, leading_zero=True):
    prefix, area_code, phone_number, info = info_tuple

    rv = ""
    if country:
        if leading_zero and prefix:
            rv = "+49 (" + prefix + ")"
        else:
            rv = "+49 "
    elif prefix:
        rv += prefix

    if prefix:
        if not area_code:
            raise RuntimeError("Invalid state - prefix but NO area_code defined - " + str(info_tuple))
        if not phone_number:
            raise RuntimeError("Invalid state - prefix but ONLY area code defined - " + str(info_tuple))
        rv += area_code + " " + phone_number
    else:
        if area_code:
            rv += area_code + " "
        rv += phone_number

    return rv


def format(number, country=True, leading_zero=True):
    return format_split(split(number), country=country, leading_zero=leading_zero)
