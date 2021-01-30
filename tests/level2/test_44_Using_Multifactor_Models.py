import unittest

from src.level2.portfolio_managment import multifactor_models
import pandas as pd




# Testing CFA II 2020 Reading 44 : Using Multifactor Models on curriculum examples


class TestAssociates(unittest.TestCase):
    def test_APT(self):
        # Example 2

        data = {'Portfolio': ['A', 'B', 'C', 'D'],
                'Expected Return': [0.0750, 0.1500, 0.0700, 0.0800],
                'Factor Sensitivity': [0.50, 2.00, 0.40, 0.45]
                }
        df = pd.DataFrame(data, columns=['Portfolio', 'Expected Return', 'Factor Sensitivity'])
        output = multifactor_models.check_arbitrage(df)
        self.assertAlmostEqual(output, 'A', places=2, msg='Example 1.1 failed')

        # Example 3

        data = {'Stock': ['MANM', 'NXT'],
                'weight': [1/3, 2/3],
                'a_i': [0.09, 0.12],
                'b_i1': [-1, 2],
                'b_i2': [1, 4]
                }
        df = pd.DataFrame(data, columns=['Stock', 'weight', 'a_i', 'b_i1', 'b_i2'])
        portfolio = multifactor_models.MacroFacModels(df)
        portfolio.return_sym()
        portfolio.return_value(F_INFL=0.01, F_GDP=0, eps_MANM=0.05, eps_NXT=0.05)

        self.assertAlmostEqual(output, 'A', places=2, msg='Example 1.1 failed')
if __name__ == '__main__':
    unittest.main()
