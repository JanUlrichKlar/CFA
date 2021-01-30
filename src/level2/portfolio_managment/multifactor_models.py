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


class MacroFacModels:
    """
            A class to represent a macro factor models (MFM).

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

    def return_value(self, **kwargs):
        for kwar in kwargs:
            print(type(kwar))
        free_sym = self.return_symbolic.free_symbols
        a = list(filter(None, free_sym))
        print(a)
        for free_symbol in a:
            b = free_symbol
            print(b)



        print(list(free_sym)[0])
        #print(self.return_symbolic.evalf(subs={F_INFL:0.01, F_GDP:0, eps_MANM:0.05, eps_NXT:0.05}))







def check_arbitrage(data):
    print(data)
    # Get all combinations of two portfolios of dataframe
    # and length 2
    all_combs = combinations(range(len(data.iloc[:, 0])), 2)
    comb_list = []
    for i, value in enumerate(list(all_combs)):
        comb_list = comb_list + [value]
    # for j, value in enumerate(list(all_combs)):
    del all_combs
    # initialize zero
    res = np.zeros((len(comb_list), 2))
    # Print the obtained combinations
    # comb_list = []
    for i, value in enumerate(comb_list):
        comb_list = comb_list + [value]
        a = np.array([[1] * 2, list(data.iloc[list(value), 2])]).transpose()
        b = np.array(list(data.iloc[list(value), 1]))
        res[i, :] = np.linalg.solve(a, b)
    res = np.round_(res, 10)
    unique_rows, indices = np.unique(res, axis=0, return_index=True)
    n_ind = 0
    for row in unique_rows:
        ind = np.where((res[:, 0] == row[0]) & (res[:, 1] == row[1]))
        if len(ind[0]) > n_ind:
            n_ind = len(ind[0])
            indices = ind[0]
    res_list = [comb_list[i] for i in indices]
    res_list = list(chain.from_iterable(res_list))
    res_list = list(set(res_list))
    print('no arbitrage for Portfolio:', *data['Portfolio'][res_list], sep=', ')
    print('Risk-free-rate:      ', res[indices[0], 0])
    print('factor risk premium: ', res[indices[0], 1])
    data_index_list = [i for i in range(len(data.index))]
    main_list = np.setdiff1d(data_index_list, res_list)
    print('arbitrage for Portfolio:', *data['Portfolio'][main_list], sep=', ')






    return data['Portfolio'][0]

