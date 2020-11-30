#!/usr/bin/env python

"""Main module."""

import re

from .vorwahlen import vorwahlen


def format(number, country=True, leading_zero=True):
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
            city = info[1]
            if info[2]:
                area_code = nr_[:(cnt + info[2])]
            phone_number = nr_[(cnt+info[2]):]
            break
    else:
        return None

    formatted_number = ""
    if country:
        formatted_number = "+49 (0)" if leading_zero else "+49 "
    else:
        formatted_number = "0"
    formatted_number += area_code + " " + phone_number

    return formatted_number, city
