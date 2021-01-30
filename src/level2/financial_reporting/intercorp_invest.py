#!/usr/bin/python3

# Copyright 2020 Jan-Ulrich Klar @JanUlrichKlar in GitHub
# See LICENSE for details.

from datetime import datetime, date
import json
from random import randint

import pandas as pd
import numpy as np
from datetime import datetime, date


class FinancialAssets:
    """
            A class to represent a forward rate agreement (FRA).

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

    def __init__(self, **kwargs):
        allowed_keys = {'name', 'type', 'measured', }
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        if not hasattr(self, 'gamma_c'):
            self.gamma_c = 0
        if not hasattr(self, 'theta_c'):
            self.theta_c = 0
        if not hasattr(self, 'gamma'):
            self.gamma = [[0], [0]]
        if not hasattr(self, 'theta'):
            self.theta = [[0], [0]]
        if not hasattr(self, 'f_0'):
            self.f_0 = 0
        if not hasattr(self, 'f_t'):
            self.f_t = 0
        if not hasattr(self, 'value_t'):
            self.value_t = 0

    def f0(self):

        if hasattr(self, 'r_c'):
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


class Associates:
    def __init__(self, **kwargs):
        allowed_keys = {'name', 'interest', 'initial_cost', 'income', 'dividends', 'data'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        if not hasattr(self, 'name'):
            self.name = None
        if not hasattr(self, 'equity'):
            self.equity = None
        if not hasattr(self, 'interest'):
            self.interest = None
        if not hasattr(self, 'initial_cost'):
            self.initial_cost = None
        if not hasattr(self, 'income'):
            self.income = None
        if not hasattr(self, 'dividends'):
            self.dividends = None
        if hasattr(self, 'data'):
            for column in kwargs['data']:
                # Select column contents by column name using [] operator
                if column == 'dividends':
                    self.dividends = kwargs['data'][column]
                elif column == 'income':
                    self.income = kwargs['data'][column]
            print(self.dividends)

    def value(self, **kwargs):
        if 'date' in kwargs:
            date_value = kwargs['date']
        else:
            date_value = self.income.index[-1]

        print(date_value)
        if len(self.interest.index) == 1:
            day_of_year = self.interest.index[0].timetuple().tm_yday
            print("Day of year: ", day_of_year, "\n")
            year_fac = (365 - (day_of_year - 1)) / 365
            # print(year_fac)
            # print(type(self.interest.index[0].year))
            d = datetime(self.interest.index[0].year, 12, 31)
            # for index, value in self.income.items():

            self.equity = self.initial_cost + \
                self.income[d:self.income.index[-1]].sum() * self.interest / 100 - \
                self.dividends[d:self.income.index[-1]].sum() * \
                self.interest / 100

        # print(self.equity)
        # self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        # if self.NA is not None and self.L_h is not None and self.m is not None:
        #     self.interest = self.NA * (self.L_h / 100 * self.m / self.NTD)
        # else:
        #     raise ValueError('NA, m or L_H is not defined')
