# Imports
from dataclasses import dataclass

# Class Calculator using dataclass annotation
@dataclass
class Calculator:

    # Instance Variables
    age: int
    yearly_income: float
    yearly_savings: float
    balance_401k: float
    current_contribution_401k: float
    match_percentage_401k: float
    portfolio_mix: str
    primary_card_interest_rate: float
    primary_card_debt: float
    secondary_card_interest_rate: float
    secondary_card_debt: float
    cc_interest_rate = 0
    cc_debt = 0
    money_allocation = {"Debt": 0, "Invest": 0}
    expected_portfolio_returns =    {
                                        "20/80": {"Equity": 20, "Fixed Income": 80, "ROI %": 5.95}, 
                                        "40/60": {"Equity": 40, "Fixed Income": 60, "ROI %": 6.57},
                                        "60/40": {"Equity": 60, "Fixed Income": 40, "ROI %": 7.64},
                                        "80/20": {"Equity": 80, "Fixed Income": 20, "ROI %": 8.72},
                                        "100/0": {"Equity": 100, "Fixed Income": 0, "ROI %": 9.79}
                                    }
    # Intialization method to intialize variables
    def initialize(self):
        self.set_total_cc_interest_rate()
        self.set_cc_debt()
        self.set_money_allocation()
        self.set_total_investing_capital()

    # Method to set the credit card interest rate
    def set_total_cc_interest_rate(self):
        # Set the credit card interest rate by adding the interest rates together and dividing by tow
        self.cc_interest_rate = (self.primary_card_interest_rate + self.secondary_card_interest_rate)/2

    # Method to set the credit card debt
    def set_cc_debt (self):
        # Set the credit card debt by adding the debt of the two cards together
        self.cc_debt = self.primary_card_debt + self.secondary_card_debt

    # Method to set the money allocation instance variable
    def set_money_allocation(self):
        # If the interest rate percentage is higher than the expected portfolio return on investment percentage
        if self.cc_interest_rate > self.expected_portfolio_returns[self.portfolio_mix]["ROI %"]:
            # If the credit card debt is higher than the yearly savings
            if self.cc_debt > self.yearly_savings:
                # Add the yearly savings to the debt money allocation
                self.money_allocation["Debt"] = self.yearly_savings
            else:
                # Set the debt as the credit card debt
                self.money_allocation["Debt"] = self.cc_debt
                # Set the investment capital to the yearly savings minus the credit card debt
                self.money_allocation["Invest"] = self.yearly_savings - self.cc_debt

        else:
            # Set the investment capital to the yearly saving value
            self.money_allocation["Invest"] = self.yearly_savings

    # Method to set the toal investing capital    
    def set_total_investing_capital(self):
        # Get the employer match
        employer_match = self.yearly_income * (self.match_percentage_401k / 100)
        # Save the intial investing capital as variable
        investing_capital = self.money_allocation["Invest"]

        # If the investing capital is greater than or equal to the employer match
        if investing_capital >= employer_match:
            # Add the employer match to the investing capital
            self.money_allocation["Invest"] += employer_match 
 
    # Method to get the amount of taxes
    def get_tax_amount(self, is_advised =False):
        # Save the income after 401k contribution as variable
        income_after_contribution = self.yearly_income - self.money_allocation["Invest"] if is_advised else (self.current_contribution_401k/100) * self.yearly_income

        # Check if the income after the 401k contribution is within a certain bracket
        # And return the calculated tax amount
        if income_after_contribution < 11_001:
            return 0.1 * income_after_contribution 
        elif income_after_contribution >= 11_001 and income_after_contribution < 44_726:
            return (0.1 * 11_000) + (0.12 * (income_after_contribution - 11_000))
        elif income_after_contribution >= 44_726 and income_after_contribution < 95_376:
            return (0.1 * 11_000) + (0.12 * 33_725) + (0.22 * (income_after_contribution - 44_725))
        elif income_after_contribution >= 95_376 and income_after_contribution < 182_101:
            return (0.1 * 11_000) + (0.12 * 33_725) + (0.22 * 50_650) + (0.24 * (income_after_contribution - 95_375))
        elif income_after_contribution >= 182_101 and income_after_contribution < 231_251:
            return (0.1 * 11_000) + (0.12 * 33_725) + (0.22 * 50_650) + (0.24 * 86_725) + (0.32 * (income_after_contribution - 182_100))
        elif income_after_contribution >= 231_251 and income_after_contribution < 578_126:
            return (0.1 * 11_000) + (0.12 * 33_725) + (0.22 * 50_650) + (0.24 * 86_725) + (0.32 * 49_150) + (0.35 * (income_after_contribution - 231_250))
        else:
            return (0.1 * 11_000) + (0.12 * 33_725) + (0.22 * 50_650) + (0.24 * 86_725) + (0.32 * 49_150) + (0.35 * 346_875) + (0.37 * (income_after_contribution - 578_125))

    # Mehtod ot get the effective tax rate
    def get_effective_tax_rate(self, is_advised=False):
        # Return the tax amount divided by the yearly income multiplied by 100
        return (self.get_tax_amount(is_advised) / (self.yearly_income)) * 100

    # Method to get the starting monthly cost of debt
    def get_starting_monthly_cost_of_debt(self):
        # Save the primary and secondary card debt as variables
        primary_card_debt = (self.primary_card_interest_rate/100)*self.primary_card_debt
        secondary_card_debt = (self.secondary_card_interest_rate/100)*self.secondary_card_debt

        # Return the total debt divided by 12
        return round(primary_card_debt + secondary_card_debt / 12,2) 
 
    # Method to get the final debt
    def get_final_debt(self, is_advised=False):
        # Return the credit card debt minus the money allocated for debt
        return round(self.cc_debt - self.money_allocation["Debt"] if is_advised else 0,2)
    
    # Method to get the final monthly cost of debt
    def get_monthly_cost_of_debt(self, is_advised=False):
        # Return the final debt multiplied by the interest rate divided by 12
        return round((self.get_final_debt(is_advised)*(self.cc_interest_rate/100))/12,2)
    
    # Method to get the expected porfolio key based on age
    def get_portfolio_key (self):
        # Save the keys as a list
        keys = list(self.expected_portfolio_returns.keys())
        # Set the starting index to zero
        index = 0 

        # If the age is within a range
        # Set the index to the proper portfolio key
        if self.age < 30: 
            index = 4
        elif self.age < 40:
            index = 3
        elif self.age < 50:
            index = 2
        elif self.age < 60:
            index = 1

        # Return the key
        return keys[index]

    # Method to get the portoflio ending balance
    def get_portfolio_ending_balance(self, is_advised=False):
        # Save the additional contribution, total 401k balance, portfolio mix and roi as variables
        additional_contribution = self.money_allocation["Invest"] if is_advised else (self.current_contribution_401k/100) * self.yearly_income
        total_401k_balance = self.balance_401k + additional_contribution  
        mix = self.get_portfolio_key() if is_advised else self.portfolio_mix
        roi = 1 + (self.expected_portfolio_returns[mix]["ROI %"] / 100)
        
        # Return the roi multiplied by the total 401k balance
        return round(roi * total_401k_balance,2)
    
    # Method to get the simplified net worth
    def get_simplified_net_worth(self):
        # Save the unadvised and advised ending balances
        unadvised_ending_balance = self.get_portfolio_ending_balance() - self.get_final_debt()
        advised_ending_balance = self.get_portfolio_ending_balance(True) - self.get_final_debt()

        # Return both ending balances as a list
        return [unadvised_ending_balance,advised_ending_balance]