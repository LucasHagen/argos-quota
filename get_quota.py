#!/usr/bin/env python3

import urllib.request
import math
import re

def main():
    try:
        fp = urllib.request.urlopen("https://quota.wohnheim.uni-kl.de/")
        quota_bytes = fp.read()

        quota_html = quota_bytes.decode("utf8")
        fp.close()
    except:
        print_error()

    regex_template = "<!--Wohnheime_{}-->([0-9]+(?:\.[0-9]+)?)([a-zA-Z ]+)<!--end-->[^0-9]+([0-9]+(?:\.[0-9]+)?)([a-zA-Z ]+)"

    incoming_re = re.compile(regex_template.format("incoming"))
    outgoing_re = re.compile(regex_template.format("outgoing"))

    re1 = incoming_re.search(quota_html)
    re2 = outgoing_re.search(quota_html)

    if (not re1) or (not re2):
        print_error()

    in_curr = convert_to_kb(re1.group(1), re1.group(2).strip())
    in_max  = convert_to_kb(re1.group(3), re1.group(4).strip())

    out_curr = convert_to_kb(re2.group(1), re2.group(2).strip())
    out_max  = convert_to_kb(re2.group(3), re2.group(4).strip())

    in_usage  = int((in_curr / in_max) * 100)
    out_usage = int((out_curr / out_max) * 100)

    print(f"<span color='limegreen'>{in_usage}%⇃</span><span color='red'>↾{out_usage}%</span>")
    print("---")

    print("Wohnheim Quota usage:")
    print(f"<span color='green'>In:     {re1.group(1)} {re1.group(2).strip()} / {re1.group(3)} {re1.group(4).strip()}</span>")
    print(f"<span color='red'>Out: {re2.group(1)} {re2.group(2).strip()} / {re2.group(3)} {re2.group(4).strip()}</span>")


"""
Converts the given quota usage to KiB
"""
def convert_to_kb(number, unit):
    return float(number) * unit_to_mult(unit)


"""
Gets the unit multiplier for the specific unit
"""
def unit_to_mult(unit):
    mult = 1

    if unit == "MiB":
        mult = math.pow(1024, 2)
    elif unit == "GiB":
        mult = math.pow(1024, 3)

    return mult


"""
Prints the error message and exits the program
"""
def print_error():
        print(f"<span color='limegreen'>?? ⇃</span><span color='red'>↾ ??</span>")
        print("---")

        print("Wohnheim Quota usage:")
        print("")
        print("Unable to retrieve information")
        exit(1)


if __name__ == "__main__":
    main()
