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


class FRA:
    """
        A class to represent a forward rate agreement (FRA).

        ...

        Attributes
        ----------
        NA : float
            notional amount, quantity of funds initially deposited
        h : int
            FRA expires in h days
        m : int
            Libor deposit has m days to maturity at expiration of the FRA
        g : int
            days from initiation to valuation
        L_h : float
            Libor on expiration of FRA for m days (used to calculate the interest for deposit)
        L_0 : 2D-Array
            [[0, h, m], [h, h+m]] with first row [0, h, m] and second row with libor at [h, h+m]
        L_g : 2D-Array
            [[g, h, m], [h, h+m]] with first row [g, h, m] and second row with libor at [h, h+m]
        FRA_0 : float
            initial Forward rate (calculated from L_0)
        FRA_g : float
            forward rate g days after initiation to offset FRA_0 (calculated from L_g)
        interest : float
            interest for a m day deposit at h with L_h interest rate
        D_h : float
            discount rate for advanced set, advanced settled to determine payment at expiration
        pay_set : float
            payment for advanced set, advanced settled at expiration
        value_g : float
            value of FRA at g days after initiation
        NTD : int
            number of total days in a year, used for interest calculations (always 360 in the Libor market)

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
        allowed_keys = {'NA', 'h', 'm', 'L_h', 'FRA_0', 'FRA_g', 'value_g', 'interest',
                        'pay_set', 'D_h', 'g', 'L_0', 'L_g', 'NTD'}
        self.__dict__.update(dict(zip(allowed_keys, [None] * len(allowed_keys))))
        self.NTD = 360
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def fra(self, libor):
        if libor[0][0] == 0:
            self.L_0 = libor
            if self.L_0 is not None:
                self.FRA_0 = ((1 + self.L_0[1][1] / 100 * (
                            (self.L_0[0][1] + self.L_0[0][2] - self.L_0[0][0]) / self.NTD)) /
                              (1 + self.L_0[1][0] / 100 * ((self.L_0[0][1] - self.L_0[0][0]) / self.NTD)) - 1) / \
                             (self.L_0[0][2] / self.NTD) * 100
        else:
            self.L_g = libor
            self.g = self.L_g[0][0]
            if self.L_g is not None:
                self.FRA_g = ((1 + self.L_g[1][1] / 100 * (
                            (self.L_g[0][1] + self.L_g[0][2] - self.L_g[0][0]) / self.NTD)) /
                              (1 + self.L_g[1][0] / 100 * ((self.L_g[0][1] - self.L_g[0][0]) / self.NTD)) - 1) / \
                             (self.L_g[0][2] / self.NTD) * 100

    def calc_interest(self, **kwargs):
        allowed_keys = {'NA', 'm', 'L_h'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        if self.NA is not None and self.L_h is not None and self.m is not None:
            self.interest = self.NA * (self.L_h / 100 * self.m / self.NTD)
        else:
            raise ValueError('NA, m or L_H is not defined')

    def payment(self, **kwargs):
        allowed_keys = {'NA', 'FRA_0', 'm', 'L_h', 'D_h'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        if self.NA is not None and self.L_h is not None and \
                self.m is not None and self.FRA_0 is not None and self.D_h is not None:
            self.pay_set = self.NA * ((self.FRA_0 - self.L_h) / 100 * self.m / self.NTD) / (
                    1 + (self.D_h / 100) * self.m / self.NTD)

    def value(self, **kwargs):
        allowed_keys = {'NA', 'FRA_0', 'FRA_g', 'm', 'L_h', 'D_h', 'g', 'h', 'L_0', 'L_g'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        if 'L_0' in kwargs:
            print(self.L_0)
            self.fra(self.L_0)
        if 'L_g' in kwargs:
            self.fra(self.L_g)

        if self.NA is not None and self.FRA_0 is not None and \
                self.h is not None and self.m is not None and self.g is not None \
                and self.FRA_g is not None and self.D_h is not None:
            self.value_g = self.NA * ((self.FRA_g - self.FRA_0) / 100 * self.m / self.NTD) / (
                    1 + (self.D_h / 100) * (self.h + self.m - self.g) / self.NTD)


class FixedIncomeForward:
    """
        A class to represent a fixed income forward (FIF).

        ...

        Attributes
        ----------
        NAD : int
            denotes the number of accrued days since the last coupon payment
        NTD : int
            denotes the number of total days during the coupon payment period
        n : int
            denotes the number of coupon payments per year
        C : float
            the stated annual coupon amount
        F_0 : float
            Future value of underlying adjusted for carry cash flows FV_0,T(S_0 + θ_0 – γ_0)
        B_0 : float
            Quoted bond price B0(T + Y)
        S_0 : float
            Quoted bond price + Accrued interest = B_0(T + Y) + AI_0
        QF_0 : float
            quoted futures price
        CF : float
            conversion factor
        AI_0 : float
            Accrued interest at 0
        AI_T : float
            Accrued interest at T
        FVCI : float
            future value of coupons
        PVCI : float
            present value of coupons


    """

    def __init__(self, **kwargs):
        allowed_keys = {'NAD', 'NTD', 'n', 'C', 'F_0', 'F_t' 'B_0', 'S_0', 'QF_0',
                        'CF', 'AI_0', 'AI_T', 'FVCI', 'PVCI', 'r', 'T', 'contract_value',
                        'n_contracts', 'par', 'V_t'}
        self.__dict__.update(dict(zip(allowed_keys, [None] * len(allowed_keys))))
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def f0(self, **kwargs):
        allowed_keys = {'B_0', 'AI_0', 'AI_T', 'FVCI', 'CF', 'r', 'T'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        if self.B_0 is not None and self.AI_0 is not None and \
                self.AI_T is not None and self.FVCI is not None and self.CF is not None:
            self.F_0 = (1 + self.r / 100) ** self.T * (self.B_0 + self.AI_0) - self.AI_T - self.FVCI
            if self.CF is not None:
                self.QF_0 = 1 / self.CF * self.F_0

    def value(self, **kwargs):
        allowed_keys = {'F_0', 'F_t', 'r', 'T'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        if self.F_0 is not None and self.F_t is not None and \
                self.r is not None and self.T:
            self.V_t = (1 + self.r / 100) ** self.T * (self.F_t - self.F_0)


class CurrencyContracts:
    """
        A class to represent a Currency Forward and Futures Contracts (CFC).

        ...

        Attributes
        ----------
        curr_pair : string
            denotes the domestic(DC) and the foreign currency(FC) DC/FC
        r_d : int
            denotes the number of total days during the coupon payment period
        r_f : int
            denotes the number of coupon payments per year
        T : float
            the stated annual coupon amount



    """

    def __init__(self, **kwargs):
        allowed_keys = {'curr_pair', 'S_0', 'F_0', 'r_d', 'r_f', 'T_0', 'NA', 'F_t', 'V_t',
                        'S_t', 'r_d_t', 'r_f_t', 'T_t'}
        self.__dict__.update(dict(zip(allowed_keys, [None] * len(allowed_keys))))
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def calc(self, **kwargs):
        allowed_keys = {'curr_pair', 'S_0', 'F_0', 'r_d', 'r_f', 'T_0', 'NA', 'F_t', 'V_t',
                        'S_t', 'r_d_t', 'r_f_t', 'T_t'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        # calc missing value in F_0
        my_sym = {}
        known_var = {}
        # create symbolic variables for the equation
        f_0_keys = {'S_0', 'F_0', 'r_d', 'r_f', 'T_0'}
        for var_sym in f_0_keys:
            my_sym[var_sym] = sym.symbols(var_sym)
        for attribute, value in self.__dict__.items():
            if value is None and attribute in f_0_keys:
                unkown_x = attribute
            elif attribute in f_0_keys:
                known_var[my_sym[attribute]] = value
        exp = sym.Eq(-my_sym['F_0'] + (my_sym['S_0'] *
                                       (1 + my_sym['r_f'] / 100) ** my_sym['T_0'] /
                                       (1 + my_sym['r_d'] / 100) ** my_sym['T_0']), 0)
        exp = exp.subs(known_var)
        res = sym.solveset(exp, my_sym[unkown_x])
        setattr(self, unkown_x, res.args[0])
        del exp, res, f_0_keys
        # calc missing value in F_t
        my_sym = {}
        known_var = {}
        # create symbolic variables for the equation
        f_t_keys = {'S_t', 'F_t', 'r_d_t', 'r_f_t', 'T_t'}
        for var_sym in f_t_keys:
            my_sym[var_sym] = sym.symbols(var_sym)
        for attribute, value in self.__dict__.items():
            if value is None and attribute in f_t_keys:
                unkown_x = attribute
            elif attribute in f_t_keys:
                known_var[my_sym[attribute]] = value
        exp = sym.Eq(-my_sym['F_t'] + (my_sym['S_t'] *
                                       (1 + my_sym['r_f_t'] / 100) ** my_sym['T_t'] /
                                       (1 + my_sym['r_d_t'] / 100) ** my_sym['T_t']), 0)
        exp = exp.subs(known_var)
        res = sym.solveset(exp, my_sym[unkown_x])
        setattr(self, unkown_x, res.args[0])
        del exp, res, f_t_keys

        # calc missing value in V_t
        my_sym = {}
        known_var = {}
        # create symbolic variables for the equation
        v_t_keys = {'F_0', 'F_t', 'r_f_t', 'T_t', 'V_t'}
        for var_sym in v_t_keys:
            my_sym[var_sym] = sym.symbols(var_sym)
        for attribute, value in self.__dict__.items():
            if value is None and attribute in v_t_keys:
                unkown_x = attribute
            elif attribute in v_t_keys:
                known_var[my_sym[attribute]] = value
        exp = sym.Eq(-my_sym['V_t'] + (my_sym['F_0'] - my_sym['F_t']) *
                     (1 + my_sym['r_f_t'] / 100) ** my_sym['T_t'], 0)
        exp = exp.subs(known_var)
        res = sym.solveset(exp, my_sym[unkown_x])
        setattr(self, unkown_x, res.args[0])
        del exp, res, v_t_keys


class InterestRateSwap:
    """
        A class to represent a Intererst Rate Swap Contracts (CFC).

        ...

        Attributes
        ----------
        curr_pair : string
            denotes the domestic(DC) and the foreign currency(FC) DC/FC
        r_d : int
            denotes the number of total days during the coupon payment period
        r_f : int
            denotes the number of coupon payments per year
        T : float
            the stated annual coupon amount



    """

    def __init__(self, **kwargs):
        allowed_keys = {'PV', 'r_fix', 'r_fix_t', 'v_t', 'PV_t'}
        self.__dict__.update(dict(zip(allowed_keys, [None] * len(allowed_keys))))
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def calc(self, **kwargs):
        allowed_keys = {'PV', 'r_fix', 'r_fix_t', 'v_t', 'PV_t'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        # calc r_fix
        if self.r_fix is None:
            setattr(self, 'r_fix', (1 - self.PV.iloc[-1, 1]) / self.PV.iloc[:, 1].sum())
        if self.r_fix_t is None and self.PV_t is not None:
            setattr(self, 'r_fix_t', (1 - self.PV_t.iloc[-1, 1]) / self.PV_t.iloc[:, 1].sum())
        if self.v_t is None and self.PV_t is not None and \
                self.r_fix is not None and self.r_fix_t is not None:
            setattr(self, 'v_t', (self.r_fix - self.r_fix_t) * self.PV_t.iloc[:, 1].sum())


class CurrencySwap:
    """
        A class to represent a Currency Swap Contracts (CSC).

        ...

        Attributes
        ----------
        na        : dict
            denotes the notional amount (NA) {'USD': 100, 'EUR': 95}
        curr_pair : dict
            denotes the domestic(DC) and the foreign currency(FC) FC/DC {DC: 'USD', FC: 'AUD'}
        ntd : int
            default 360
        exchange_rate : dict
            denotes  the exchange rate {AUD/USD: 1.140}
        spot_rate : dict
            {NAD: [90, 180, 270, 360], AUD: [2.50, 2.60, 2.70, 2.80], USD: [0.10, 0.15, 0.20, 0.25]}
        pv        : dict
            {NAD: [90, 180, 270, 360], AUD: [0.993789, 0.987167, 0.980152, 0.972763],
            USD: [0.10, 0.15, 0.20, 0.25]}
        r_fix    : dict
            {AUD: 0.0277, USD:0.0025}




    """

    def __init__(self, **kwargs):
        allowed_keys = {'na', 'curr_pair', 'ntd', 'exchange_rate', 'spot_rates', 'pv', 'r_fix', 'fixed_pay'}
        self.__dict__.update(dict(zip(allowed_keys, [{}] * len(allowed_keys))))
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        if 'FC' in self.curr_pair and 'DC' in self.curr_pair \
                and isinstance(self.curr_pair['FC'], str) and isinstance(self.curr_pair['DC'], str):
            pass
        else:
            print('Currency pair must be specified as dictionary \
                  {''DC'': ''EUR'', ''FC'': ''USD''}')
            raise TypeError
        # if fixed rates are not specified try to calculate from
        # pv (present values) or first pv from spot_rates
        if len(self.r_fix) != 2:
            print('No fixed rates specified. Trying to calculate')
            # no pv then try to calculate from spot_rates
            self.calc_r_fix()
        # Calculate notional amount na
        self.calc_na()

        # calculate fixed swap payments
        self.fixed_pay = dict()
        self.calc_fixed_pay()

    def calc_r_fix(self):
        for curr in self.curr_pair.values():
            if len(self.pv) != 3 and len(self.spot_rates) == 3:
                self.pv['NAD'] = self.spot_rates['NAD']
                self.pv[curr] = 1 / (1 + (np.array(self.spot_rates[curr]) / 100 *
                                          np.array(self.spot_rates['NAD']) / 360))
                self.pv[curr] = self.pv[curr].tolist()
            elif len(self.pv) == 0 and len(self.spot_rates) == 0:
                print('Neither fixed rates nor present values nor interest rates are specified!')
                raise TypeError

            self.r_fix[curr] = (1 - np.array(self.pv[curr][-1])) / \
                               np.array(self.pv[curr]).sum() * 360 / \
                               (self.pv['NAD'][1] - self.pv['NAD'][0])

    def calc_na(self):
        if len(self.na) == 0:
            print('Notional amount not specified. ')
        elif len(self.na) != 0:
            # correct exchange rate if necesary
            if list(self.exchange_rate.keys())[0].split('/')[1] == self.curr_pair['FC']:
                ex_rate = self.exchange_rate[list(self.exchange_rate.keys())[0]]
            else:
                ex_rate = 1 / self.exchange_rate[list(self.exchange_rate.keys())[0]]

            if self.na[self.curr_pair['DC']] is None:
                self.na[self.curr_pair['DC']] = self.na[self.curr_pair['FC']] * ex_rate

            elif self.na[self.curr_pair['FC']] is None:
                self.na[self.curr_pair['FC']] = self.na[self.curr_pair['DC']] * (1 / ex_rate)

    def calc_fixed_pay(self):
        self.fixed_pay[self.curr_pair['FC']] = self.na[self.curr_pair['FC']] * self.r_fix[self.curr_pair['FC']] * \
                                               (self.pv['NAD'][1] - self.pv['NAD'][0]) / 360
        self.fixed_pay[self.curr_pair['DC']] = self.na[self.curr_pair['DC']] * self.r_fix[self.curr_pair['DC']] * \
                                               (self.pv['NAD'][1] - self.pv['NAD'][0]) / 360













    def calc(self, **kwargs):
        pass
        # allowed_keys = {'data_ir', 'data_pv'}
        # self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        # if self.curr_pair is None:
        #     self.get_curr_pair()
        # # calc PV
        # if self.data_pv is None and self.data_ir is not None:
        #     self.data_pv = self.data_ir.rename(
        #         columns={list(self.data_ir.columns)[1]:
        #                      self.curr_pair[0] + ' Present Value',
        #                  list(self.data_ir.columns)[2]:
        #                      self.curr_pair[1] + ' Present Value'})
        #     increment = self.data_pv.iloc[1, 0] - self.data_pv.iloc[0, 0]
        #     for i in range(1, 3):
        #         self.data_pv.iloc[:, i] = 1 / (1 + (self.data_pv.iloc[:, i] / 100 *
        #                                             self.data_pv.iloc[:, 0] / 360))
        #
        #         self.r_fix[self.curr_pair[i - 1]] = (1 - self.data_pv.iloc[-1, i]) / \
        #                                             self.data_pv.iloc[:, i].sum() * 360 / increment
        #
        #     print(self.r_fix)


def equity_swap(**kwargs):
    df = pd.DataFrame(kwargs, index=[0])

    cf = df['NA'] * (df['equity_return'] - df['pay_fixed']) / 100
    print(type(cf[0]))

    print('cash flow for receive-equity (pay-fixed) {:>15}'.format(cf[0]))
    print('cash flow for receive-fixed (pay-equity) {:>15}'.format(-cf[0]))


def fixed_rate(df):
    return (1 - df[-1]) / sum(df)
