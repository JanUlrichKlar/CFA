#!/usr/bin/python3

# Copyright 2020 Jan-Ulrich Klar @JanUlrichKlar in GitHub
# See LICENSE for details.

from datetime import datetime, date
import json
from random import randint

import pandas as pd
import numpy as np


class Company:
    """
            A class to represent a general company.

            ...

            Attributes
            ----------
            name : string
                name of company
            isin : string
                ISIN number


            Methods
            -------
            fra(libor):
                calculates FRA_0 if libor is L_0 and FRA_g if libor is L_g respectively


                """
    def __init__(self, **kwargs):
        allowed_keys = {'name', 'isin'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        if not hasattr(self, 'name'):
            self.name = None
        if not hasattr(self, 'isin'):
            self.isin = None