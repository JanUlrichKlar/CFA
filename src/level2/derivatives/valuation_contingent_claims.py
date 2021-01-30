#!/usr/bin/python3

# Copyright 2020 Jan-Ulrich Klar @JanUlrichKlar in GitHub
# See LICENSE for details.

from datetime import datetime, date
import json
from random import randint

import pandas as pd
import numpy as np
import sympy as sym

class EquityForward:
    """
        This function calculates the equity forward price and values at a certain point in time\n
        Accepted Parameters are:\n
        s_0    : spot price at initialization\n
        f_0    : future price at initialization\n
        r      : risk-free rate in percentage\n
        r_c    : continuous risk-free rate in percentage\n
        t_0_exp: days from initialization to expiration\n
        t      : time from initialization to valuation\n
        s_t    : spot price at valuation\n
        gamma  : 2d list of benefits and days from initialization [[D1, D2, ... ], [t_D1, t_D2, ...]\n
        Example: Dividend D1 and D2 payed in 30 and 120 days[[D1, D2],[30, 120]]\n
        theta  : 2d list of costs and days from initialization[[C1, C2, ... ], [t_C1, t_C2, ...]\n
        gamma_c: continuous benefits in percentage\n
        theta_c: continuous costs in percentage\n

        Parameters:
             kwargs:
        Returns:
            :obj:`pandas.Series` - ds:
                The resulting :obj:`pandas.Series` contains all inputs and possible results. If no parameter t and s_t
                is specified no valuation

                So on, the resulting :obj:`pandas.Series` will look like::

                s_0 : XXX
                f_0 : XXX
                s_t : XXX

        Raises:
            ValueError: raised whenever any of the introduced arguments is not valid.


        """

    def __init__(self, **kwargs):
        allowed_keys = {'s_0', 's_t', 't', 't_0_exp', 'r', 'r_c', 'gamma', 'theta', 'gamma_c', 'theta_c',
                        'f_0', 'f_t', 'value_t'}
        self.__dict__.update(dict(zip(allowed_keys, [None] * len(allowed_keys))))
        self.gamma, self.theta = [[0], [0]], [[0], [0]]
        self.gamma_c, self.theta_c = 0, 0
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def f0(self):

        if self.r_c is not None:
            self.f_0 = self.s_0 * np.exp((self.r_c + self.theta_c - self.gamma_c) / 100 * (self.t_0_exp / 360))

        else:
            gamma_0 = 0
            for (gam, t) in zip(self.gamma[0], self.gamma[1]):
                # print(gam)
                # print(t)
                gamma_0 = gamma_0 + gam / (1 + self.r / 100) ** (t / 360)
            # print(gamma_0)

            theta_0 = 0
            for (thet, t) in zip(self.theta[0], self.theta[1]):
                theta_0 = theta_0 + thet / (1 + self.r / 100) ** (t / 360)
            self.f_0 = (self.s_0 + theta_0 - gamma_0) * (1 + self.r / 100) ** ((self.t_0_exp) / 360)

    def value(self):
        # calculate f_t and value of contract if 't' is in the inputs
        if hasattr(self, 't') and hasattr(self, 's_t'):
            self.f_t = self.s_t * (1 + self.r / 100) ** ((self.t_0_exp - self.t) / 360)
            self.value_t = (self.f_t - self.f_0) / (1 + self.r / 100) ** ((self.t_0_exp - self.t) / 360)
