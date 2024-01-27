# Imports
import pandas as pd
import numpy as np
import os
from dataclasses import dataclass
from calculator import Calculator
from pathlib import Path
from plotnine import ggplot, geom_line, labs, aes

# Class Projector using dataclass annotation
@dataclass
class Projector:

    # Instance variables
    calc: Calculator
    debt = 0
    portfolio_balance = 0
    projection_data = pd.DataFrame(
        {
            "Simplified Net Worth": np.nan,
            "Year-End Debt": np.nan,
            "Investing Capital": np.nan,
            "Ending 401k Balance": np.nan,
            "Year": range(1,6)
        }
    )

    # Intialization method to intialize variables
    def initialize(self):
        self.debt = self.calc.get_final_debt(True) 
        self.portfolio_balance = self.calc.get_portfolio_ending_balance(True)
        self.get_data()


    # Method to pull data and add it to the dataframe
    def get_data(self):
        # Starting row
        row = 0
        # Set first row of data
        self.projection_data.iloc[row,0] = self.calc.get_simplified_net_worth()[1]
        self.projection_data.iloc[row,1] = self.debt
        self.projection_data.iloc[row,2] = self.calc.money_allocation["Invest"]
        self.projection_data.iloc[row,3] = self.portfolio_balance
        
        # Loop four times from 1-4
        for i in range(1,5):
            # Set each row of data on each new loop
            self.projection_data.iloc[i, 1:3] = self.get_next_final_debt()
            self.projection_data.iloc[i, 3] = self.get_next_portfolio_ending_balance()
            self.projection_data.iloc[i, 0] = self.get_next_simplified_net_worth()
        

    # Method to get next value for final debt
    def get_next_final_debt(self):
        # Set variables for method and within calculator
        investment_capital = self.calc.money_allocation["Invest"]
        self.calc.cc_debt = self.debt 
        self.debt =  self.calc.get_final_debt(True)

        # If the debt value is less than zero
        if self.debt < 0:
            # Add inverse of self debt to investment capital
            investment_capital += self.debt*-1
            # Set debt to zero
            self.debt = 0

        # Return debt and investment capital
        return [self.debt, investment_capital]

    # Merthod to get the next portfolio ending balance
    def get_next_portfolio_ending_balance(self):
        # Set calkculator 401k balance and class variable porfolio balance
        self.calc.balance_401k = self.portfolio_balance
        self.portfolio_balance = self.calc.get_portfolio_ending_balance(True)

        # Return portfolio balance
        return self.portfolio_balance
    
    # Method to get the next simplified net worth
    def get_next_simplified_net_worth(self):
        # Return the advised simplified net worth from the calculator
        return self.calc.get_simplified_net_worth()[1]

    # Method to create/save plot and return path
    def get_save_line_plot(self, y_value):
        # Create plot
        plot = (
            ggplot(self.projection_data, aes(x='Year', y=y_value))
            + geom_line()
            + labs(x='Year', y=y_value, title=f"Projected {y_value} Over The Next 5 Years")
        )

        # Save plot path
        path = Path(f"./assets/images/plots/{y_value.replace(' ', '_')}.png")

        # If the file exists
        if path.is_file():
            # Delete the file
            os.remove(path)

        # Save the plot as an image
        plot.save(path)

        # Return the path
        return path
    
    # Method to get all image paths
    def get_image_paths(self):
        # List to hold paths
        paths = []

        # Look over columns
        for i in self.projection_data.columns.values[:-1]:
            # Append path the paths list
            paths.append(self.get_save_line_plot(i))

        # Return paths list
        return paths

