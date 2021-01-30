#!/usr/bin/python3

# Copyright 2020 Jan-Ulrich Klar @JanUlrichKlar in GitHub
# See LICENSE for details.

from datetime import datetime, date
import json
from random import randint

import pandas as pd
import numpy as np
from itertools import combinations, chain
import sympy as sym

from datetime import datetime, date


class PrivateRealEstate:
    """
            A class to represent a Private Real Estate Investment (PRE).

            ...

            Attributes
            ----------
            type : string
                Debt or Equity
            classification : string
                AC (amortized cost),\n
                FVPL (Fair value through profit or loss),\n
                FVOCI (Fair Value through Other comprehensive income)  \n


            Methods
            -------
            fra(libor):
                calculates FRA_0 if libor is L_0 and FRA_g if libor is L_g respectively
            interest(**kwargs):
                calculates interest on deposit NA at h for m days with Libor L_h(m)
                    :keyword NA:
                    :keyword m:
                    :keyword L_h:

                """

    def __init__(self, df):
        self.portfolio = df
        self.return_symbolic = None

    def return_sym(self):
        port_return = sym.Symbol('')

        for i, row in self.portfolio.iterrows():
            port_return = port_return + sym.simplify(str(row['weight']) + '*' + str(row['a_i'])) + \
                sym.nsimplify(str(row['weight']) + '*' + str(row['b_i1']) + '*F_INFL') + \
                sym.nsimplify(str(row['weight']) + '*' + str(row['b_i2']) + '*F_GDP') + \
                sym.nsimplify(str(row['weight']) + '*' + 'eps_' + str(row['Stock']))
        self.return_symbolic = port_return
        print(type(port_return))
        print(str(port_return))