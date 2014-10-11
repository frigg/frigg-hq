# -*- coding: utf8 -*-
import re


def is_retest_comment(message):
    return bool(re.match(r'(?:[Rr]e)?[Tt]est(?: (?:now|this))? ?(?:please)?', message))
