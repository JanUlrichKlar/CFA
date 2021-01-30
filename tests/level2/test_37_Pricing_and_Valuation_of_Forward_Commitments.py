import unittest
import src.level2.derivatives.forward_commitments as fc
import pandas as pd


# Testing CFA II 2020 Reading 37 :Pricing and Valuation of Forward Commitments on curriculum examples


class TestEquityForward(unittest.TestCase):
    def test_equity(self):
        # Example 1.1
        equ = fc.EquityForward(s_0=63.31, t_0_exp=90, r=2.75)
        equ.f0()
        self.assertAlmostEqual(equ.f_0, 63.74, places=2, msg='Example 1.1 failed')
        # Example 1.2
        equ = fc.EquityForward(s_0=63.31, t_0_exp=90, r=2.25)
        equ.f0()
        self.assertAlmostEqual(equ.f_0, 63.6632, places=2, msg='Example 1.2 failed')
        # Example 2
        equ = fc.EquityForward(f_0=105.00, t_0_exp=360, t=270,
                                s_t=110.00, r=5.00)
        equ.value()
        self.assertAlmostEqual(equ.value_t, 6.2729, places=2, msg='Example 2 failed')
        # Example 3
        equ = fc.EquityForward(s_0=3500, t_0_exp=90, r_c=0.15, gamma_c=3)
        equ.f0()
        self.assertAlmostEqual(equ.f_0, 3475.15, places=2, msg='Example 3 failed')
        # Example 4
        equ = fc.EquityForward(s_0=70, t_0_exp=30, r=1, gamma=[[2.20], [30]])
        equ.f0()
        self.assertAlmostEqual(equ.f_0, 67.86, places=2, msg='Example 4 failed')
        # Example 5
        equ = fc.EquityForward(f_0=102, t_0_exp=360, t=270, s_t=110, r=5)
        equ.value()
        self.assertAlmostEqual(equ.value_t, 9.236592, places=2, msg='Example 5 failed')


class TestFRA(unittest.TestCase):
    def test_fra(self):
        # Example 6.1
        fra = fc.FRA()
        fra.calc_interest(NA=10000000, m=90, L_h=0.55)
        self.assertAlmostEqual(fra.interest, 13750, places=2, msg='Example 6.1 failed')
        # Example 6.2
        fra.payment(NA=10000000, h=30, m=90, FRA_0=0.6, L_h=0.55, D_h=0.4)
        self.assertAlmostEqual(fra.pay_set, 1248.75, places=2, msg='Example 6.2 failed')
        # Example 6.3
        #fra = fc.FRA(NA=10000000, h=30, m=90, FRA_0=0.5, L_h=0.55, D_h=0.4)
        fra.payment(FRA_0=0.5)
        self.assertAlmostEqual(fra.pay_set, -1248.75, places=2, msg='Example 6.3 failed')
        # Example 7
        fra = fc.FRA()
        fra.fra([[0, 180, 90], [1.5, 1.75]])
        self.assertAlmostEqual(fra.FRA_0, 2.23, places=2, msg='Example 7 failed')
        # Example 8
        fra = fc.FRA()
        fra.fra([[0, 180, 90], [0.628, 0.712]])
        fra.fra([[90, 180, 90], [1.25, 1.35]])
        fra.value(FRA_0=0.86, NA=10000000, g=90, h=180, m=90, D_h=1.35, L_g=[[90, 180, 90], [1.25, 1.35]])
        self.assertAlmostEqual(fra.value_g, 14651, msg='Example 8 failed', delta=14651*0.01)


class TestFixedIncome(unittest.TestCase):
    def test_fif(self):
        # Example 9
        fif = fc.FixedIncomeForward()
        fif.f0(B_0=108, AI_0=0.083, AI_T=0.25, FVCI=0, CF=0.729535, r=0.1, T=1/12)
        self.assertAlmostEqual(fif.QF_0, 147.82, places=2, msg='Example 9 failed')
        # Example 10
        fif.value(F_0=145, F_t=148, r=0.1, T=1 / 12)
        fif.contract_value = 100000
        fif.n_contracts = 5
        self.assertAlmostEqual(fif.V_t/100*fif.contract_value*fif.n_contracts, 14998.50,
                               msg='Example 10 failed', delta=14998.50*0.01)


class TestCurrencyContracts(unittest.TestCase):
    def test_cc(self):
        # Example 11.1
        cc = fc.CurrencyContracts(curr_pair='GBP/EUR', S_0=0.792, r_d=0.3, r_f=1, T_0=1)
        cc.calc()
        self.assertAlmostEqual(cc.F_0, 0.798,
                               msg='Example 11.1 failed', delta=0.798*0.01)
        cc = fc.CurrencyContracts(curr_pair='GBP/EUR', F_0=0.791, S_0=0.792, r_d=0.3, T_0=1)
        cc.calc()
        self.assertTrue(cc.r_d > cc.r_f, msg='Example 11.2 failed')
        # Example 12
        cc = fc.CurrencyContracts(curr_pair='GBP/EUR', F_0=0.8, S_t=0.75, r_d_t=0.4, r_f_t=0.8, T_t=3/12)
        cc.calc()
        self.assertAlmostEqual(cc.F_t, 0.7507,
                               msg='Example 12.1 failed', delta=0.7507 * 0.01)
        self.assertAlmostEqual(cc.V_t, 0.0492,
                               msg='Example 12.2 failed', delta=0.0492 * 0.01)


class TestInterestRateSwapContracts(unittest.TestCase):
    def test_cc(self):
        # Example 13
        data = {'Maturity': [1, 2, 3, 4, 5],
                'PV Factors': [0.990099, 0.977876, 0.965136, 0.951529, 0.937467]}
        ts_interest = pd.Series(20, index=pd.date_range('1/1/2016', periods=1, freq='T'))
        df = pd.DataFrame(data, columns=['Maturity', 'PV Factors'])
        irs = fc.InterestRateSwap(PV=df)
        irs.calc()
        self.assertAlmostEqual(irs.r_fix*100, 1.2968, msg='Example 13 failed', delta=1.2968*0.01)
        # Example 14
        irs = fc.InterestRateSwap(r_fix=0.02, PV_t=df)
        irs.calc()
        self.assertAlmostEqual(irs.v_t * 1e8, 3.375e6, msg='Example 13 failed', delta=3.375e6 * 0.01)


class TestCurrencySwapContracts(unittest.TestCase):
    def test_cc(self):
        # Example 15
        na = {'AUD': 1e8, 'USD': None}
        curr_pair = {'DC': 'USD', 'FC': 'AUD'}
        spot_rates = {'NAD': [90, 180, 270, 360], 'AUD': [2.50, 2.60, 2.70, 2.80], 'USD': [0.10, 0.15, 0.20, 0.25]}
        cs = fc.CurrencySwap(na=na, curr_pair=curr_pair, spot_rates=spot_rates, exchange_rate={'AUD/USD': 1.140})
        cs.calc()

        self.assertAlmostEqual(cs.r_fix['AUD'] * 100,
                               2.7695, msg='Example 15 failed',
                               delta=2.7695 * 0.01)
        self.assertAlmostEqual(cs.r_fix['USD'] * 100,
                               0.2497, msg='Example 15 failed',
                               delta=0.2497 * 0.01)
        self.assertAlmostEqual(cs.na['USD'] / 1e6,
                               88, msg='Example 15 failed',
                               delta=88 * 0.01)


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
# ds = fc.irate_forward(NA=10000000, i=30, m=90, L_i=0.55)
# pd.testing.assert_series_equal(ds, result_series, check_exact=False, atol=1e-3)
# print('Example 6_1 passed!')
#
# # 2
# # create expected output
# dict_res = {'NA': 10000000, 'i': 30, 'm': 90, 'FRA': 0.6, 'L_i': 0.55, 'D_h': 0.4, 'pay_set': 1248.75}
# result_series = pd.Series(dict_res)
# # check output
# ds = fc.irate_forward(NA=10000000, i=30, m=90, FRA=0.6, L_i=0.55, D_h=0.4)
# pd.testing.assert_series_equal(ds, result_series, check_exact=False, atol=1e-3)
# print('Example 6_2 passed!')
#
# # 3
# # create expected output
# dict_res = {'NA': 10000000, 'i': 30, 'm': 90, 'FRA': 0.5, 'L_i': 0.55, 'D_h': 0.4, 'pay_set': -1248.75}
# result_series = pd.Series(dict_res)
# # check output
# ds = fc.irate_forward(NA=10000000, i=30, m=90, FRA=0.5, L_i=0.55, D_h=0.4)
# pd.testing.assert_series_equal(ds, result_series, check_exact=False, atol=1e-3)
# print('Example 6_3 passed!')
#
# # Example 7
# # create expected output
# dict_res = {'L': [[180, 270], [1.5, 1.75]], 'FRA': 2.23}
# result_series = pd.Series(dict_res)
# # check output
# ds = fc.irate_forward(L=[[180, 270], [1.5, 1.75]])
# pd.testing.assert_series_equal(ds, result_series, check_exact=False, atol=1e-2)
# print('Example 7 passed!')
#
# # Example 8
# # create expected output
# dict_res = {'NA': 10000000, 'i': 180, 'm': 90, 'FRA': 0.86, 'L_i': 0.55, 'D_h': 0.4, 'pay_set': -1248.75}
# result_series = pd.Series(dict_res)
# # check output
# ds = fc.irate_forward(L=[[180, 270], [1.5, 1.75]])
# pd.testing.assert_series_equal(ds, result_series, check_exact=False, atol=1e-2)
# print('Example 7 passed!')
# #fc.equity_swap(position='re', reset='quarterly', NA=5000000, pay_fixed=0.4, equity_return=-6)
# #fixed_rate = fc.fixed_rate([0.990099, 0.977876, 0.965136, 0.951529, 0.937467])
# #print(fixed_rate)
#
# #fixed_rate = fra.ifa(type='debt', date_inv='2010-1-1', IV=240000, coupon=7, par=200000, FV=270000, r=5, )
# #print(fixed_rate)