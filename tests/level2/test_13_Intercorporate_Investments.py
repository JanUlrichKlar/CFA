import unittest

from src.level2.financial_reporting import *
import pandas as pd




# Testing CFA II 2020 Reading 13 :Intercorporate Investments on curriculum examples
print('Hello')
# associate = intercorp_invest.Associates(name='Branch', interest=20, initial_cost=200000)
# print(associate.name)


class TestAssociates(unittest.TestCase):
    def test_equity(self):
        # Example 1.1

        data = {'income': [200000, 300000, 400000],
                'dividends': [50000, 100000, 200000]
                }
        ts_interest = pd.Series(20, index=pd.date_range('1/1/2016', periods=1, freq='T'))
        df = pd.DataFrame(data, columns=['income', 'dividends'],
                          index=pd.date_range('31/12/2016', periods=3, freq='Y'))
        associate = intercorp_invest.Associates(name='Branch', interest=ts_interest,
                                                initial_cost=200000, data=df)
        associate.value()
        self.assertAlmostEqual(associate.equity.iloc[0], 310000, places=2, msg='Example 1.1 failed')
#         # Example 1.2
#         equ = der.EquityForward(s_0=63.31, t_0_exp=90, r=2.25)
#         equ.f0()
#         self.assertAlmostEqual(equ.f_0, 63.6632, places=2, msg='Example 1.2 failed')
#         # Example 2
#         equ = der.EquityForward(f_0=105.00, t_0_exp=360, t=270,
#                                 s_t=110.00, r=5.00)
#         equ.value()
#         self.assertAlmostEqual(equ.value_t, 6.2729, places=2, msg='Example 2 failed')
#         # Example 3
#         equ = der.EquityForward(s_0=3500, t_0_exp=90, r_c=0.15, gamma_c=3)
#         equ.f0()
#         self.assertAlmostEqual(equ.f_0, 3475.15, places=2, msg='Example 3 failed')
#         # Example 4
#         equ = der.EquityForward(s_0=70, t_0_exp=30, r=1, gamma=[[2.20], [30]])
#         equ.f0()
#         self.assertAlmostEqual(equ.f_0, 67.86, places=2, msg='Example 4 failed')
#         # Example 5
#         equ = der.EquityForward(f_0=102, t_0_exp=360, t=270, s_t=110, r=5)
#         equ.value()
#         self.assertAlmostEqual(equ.value_t, 9.236592, places=2, msg='Example 5 failed')
#
#
# class TestFRA(unittest.TestCase):
#     def test_fra(self):
#         # Example 6.1
#         fra = der.FRA()
#         fra.interest(NA=10000000, m=90, L_h=0.55)
#         self.assertAlmostEqual(fra.interest, 13750, places=2, msg='Example 6.1 failed')
#         # Example 6.2
#         fra.payment(NA=10000000, h=30, m=90, FRA_0=0.6, L_h=0.55, D_h=0.4)
#         self.assertAlmostEqual(fra.pay_set, 1248.75, places=2, msg='Example 6.2 failed')
#         # Example 6.3
#         #fra = der.FRA(NA=10000000, h=30, m=90, FRA_0=0.5, L_h=0.55, D_h=0.4)
#         fra.payment(FRA_0=0.5)
#         self.assertAlmostEqual(fra.pay_set, -1248.75, places=2, msg='Example 6.3 failed')
#         # Example 7
#         fra = der.FRA()
#         fra.fra([[0, 180, 90], [1.5, 1.75]])
#         self.assertAlmostEqual(fra.FRA_0, 2.23, places=2, msg='Example 7 failed')
#         # Example 8
#         fra = der.FRA()
#         fra.fra([[0, 180, 90], [0.628, 0.712]])
#         fra.fra([[90, 180, 90], [1.25, 1.35]])
#         fra.value(FRA_0=0.86, NA=10000000, g=90, h=180, m=90, D_h=1.35, L_g=[[90, 180, 90], [1.25, 1.35]])
#         self.assertAlmostEqual(fra.value_g, 14651, msg='Example 8 failed', delta=14651*0.01)
#
#
# class TestFixedIncome(unittest.TestCase):
#     def test_fif(self):
#         # Example 6.1
#         fif = der.FIF()
#         fif.f0(B_0=108, AI_0=0.083, AI_T=0.25, FVCI=0, CF=0.729535, r=0.1, T=1/12)
#         self.assertAlmostEqual(fif.QF_0, 147.82, places=2, msg='Example 9 failed')
#         fif.value(F_0=145, F_t=148, r=0.1, T=1 / 12)
#         fif.contract_value = 100000
#         fif.n_contracts = 5
#         self.assertAlmostEqual(fif.V_t/100*fif.contract_value*fif.n_contracts, 14998.50,
#                                msg='Example 10 failed', delta=14998.50*0.01)


if __name__ == '__main__':
   unittest.main()







# #***********************************************************************************************************************
# #               Interest Rate Forward and Future Contracts
# #***********************************************************************************************************************
# # Example 6
# # 1
# # create expected output
# dict_res = {'NA': 10000000, 'i': 30, 'm': 90, 'L_i': 0.55, 'Interest': 13750}
# result_series = pd.Series(dict_res)
# # check output
# ds = der.irate_forward(NA=10000000, i=30, m=90, L_i=0.55)
# pd.testing.assert_series_equal(ds, result_series, check_exact=False, atol=1e-3)
# print('Example 6_1 passed!')
#
# # 2
# # create expected output
# dict_res = {'NA': 10000000, 'i': 30, 'm': 90, 'FRA': 0.6, 'L_i': 0.55, 'D_h': 0.4, 'pay_set': 1248.75}
# result_series = pd.Series(dict_res)
# # check output
# ds = der.irate_forward(NA=10000000, i=30, m=90, FRA=0.6, L_i=0.55, D_h=0.4)
# pd.testing.assert_series_equal(ds, result_series, check_exact=False, atol=1e-3)
# print('Example 6_2 passed!')
#
# # 3
# # create expected output
# dict_res = {'NA': 10000000, 'i': 30, 'm': 90, 'FRA': 0.5, 'L_i': 0.55, 'D_h': 0.4, 'pay_set': -1248.75}
# result_series = pd.Series(dict_res)
# # check output
# ds = der.irate_forward(NA=10000000, i=30, m=90, FRA=0.5, L_i=0.55, D_h=0.4)
# pd.testing.assert_series_equal(ds, result_series, check_exact=False, atol=1e-3)
# print('Example 6_3 passed!')
#
# # Example 7
# # create expected output
# dict_res = {'L': [[180, 270], [1.5, 1.75]], 'FRA': 2.23}
# result_series = pd.Series(dict_res)
# # check output
# ds = der.irate_forward(L=[[180, 270], [1.5, 1.75]])
# pd.testing.assert_series_equal(ds, result_series, check_exact=False, atol=1e-2)
# print('Example 7 passed!')
#
# # Example 8
# # create expected output
# dict_res = {'NA': 10000000, 'i': 180, 'm': 90, 'FRA': 0.86, 'L_i': 0.55, 'D_h': 0.4, 'pay_set': -1248.75}
# result_series = pd.Series(dict_res)
# # check output
# ds = der.irate_forward(L=[[180, 270], [1.5, 1.75]])
# pd.testing.assert_series_equal(ds, result_series, check_exact=False, atol=1e-2)
# print('Example 7 passed!')
# #der.equity_swap(position='re', reset='quarterly', NA=5000000, pay_fixed=0.4, equity_return=-6)
# #fixed_rate = der.fixed_rate([0.990099, 0.977876, 0.965136, 0.951529, 0.937467])
# #print(fixed_rate)
#
# #fixed_rate = fra.ifa(type='debt', date_inv='2010-1-1', IV=240000, coupon=7, par=200000, FV=270000, r=5, )
# #print(fixed_rate)