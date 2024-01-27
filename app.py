# Imports
import streamlit as st
from projection import Projector
from calculator import Calculator
from pathlib import Path
from PIL import Image

# Method to get formatted portfolio mix
def get_formated_portfolio_mix(mix):
    # Split the mix string by the / sign
    mix = mix.split("/")

    # Return formatted portoflio mix
    return f"Stocks: {mix[0]}%, Bonds: {mix[1]}%"

# Method to get the calculatiions
def get_calculations(
    age,yearly_income,
    yearly_savings,
    balance_401k,
    current_contribution_401k,
    match_percentage_401k,
    portfolio_mix,
    primary_card_interest_rate,
    primary_card_debt,
    secondary_card_interest_rate,
    secondary_card_debt
):
    # Create a calculator instance with formatted variables
    calculator = Calculator(
        int(age),
        float(yearly_income),
        float(yearly_savings),
        float(balance_401k),
        float(current_contribution_401k),
        float(match_percentage_401k),
        portfolio_mix,
        float(primary_card_interest_rate),
        float(primary_card_debt),
        float(secondary_card_interest_rate),
        float(secondary_card_debt)
    )

    # Intialize the calculator varaibles
    calculator.initialize()
                
    # Display the current financials
    st.write("### Your Current Financials")
    st.write(f"Monthly Cost of Debt: ${calculator.get_starting_monthly_cost_of_debt()}")

    # Display the financials without advice
    st.write("### Without Advice")
    unadvised_ending_balance,advised_ending_balance = calculator.get_simplified_net_worth()
    st.write(f"Yearly Ending Balance: ${unadvised_ending_balance}")
    st.write(f"Current Debt: ${calculator.cc_debt}")
    st.write(f"Effective Tax Rate: {calculator.get_effective_tax_rate()}%")
    st.write(f"Monthly Cost of Debt: ${calculator.get_monthly_cost_of_debt()}")

    # Display the financials with advice
    st.write("### With Advice")
    st.write("We reccomend that you:")

    debt,invest = calculator.money_allocation.values()
    # If the investment captial is not zero
    if invest != 0:
        st.write(f"- Invest ${invest} in your 401k")
    else:
        st.write("- Since the interest rate on your card is higher than your expected portfolio return, we recccomend that you pay off your credit card debt first.")
    
    # If the debt capital is not zero
    if debt != 0:
        st.write(f"- Pay off ${debt} credit card debt")

    # If the selected portoflio mix is not equal to the suggested portfolio mix
    if portfolio_mix != calculator.get_portfolio_key():
        st.write(f"- Currently you have a portfolio mix of {get_formated_portfolio_mix(portfolio_mix)} and we reccomend you move to a portfolio mix of {get_formated_portfolio_mix(calculator.get_portfolio_key())}")

    # Display the rest of the financials with advice
    st.write(f"Yearly Ending Balance: ${advised_ending_balance}")
    st.write(f"Final Debt: ${calculator.get_final_debt()}")
    st.write(f"Effective Tax Rate: {calculator.get_effective_tax_rate(True)}%")
    st.write(f"Monthly Cost of Debt: ${calculator.get_monthly_cost_of_debt(True)}")

    # Return the calculator
    return calculator

# Method to display the projections
def get_projections(calculator):
    # Instantiate and initialize projector variable
    projector = Projector(calculator)
    projector.initialize()

    # Display header
    st.write("### Projections With Advice")

    # Loop over image paths
    for image_path in projector.get_image_paths():
        # Open and image
        plot_image = Image.open(Path(image_path))
        # Display plot image
        st.image(plot_image)

# Method to handle submittion
def handle_submittion(
    age,yearly_income,
    yearly_savings,
    balance_401k,
    current_contribution_401k,
    match_percentage_401k,
    portfolio_mix,
    primary_card_interest_rate,
    primary_card_debt,
    secondary_card_interest_rate,
    secondary_card_debt
):
    # If the yearly saving are greater than the current contribution
    if float(yearly_savings) > ((float(current_contribution_401k)/100) * float(yearly_income)):    
        try:
            # Get the caculator and calculations
            calculator = get_calculations(
                                age,yearly_income,
                                yearly_savings,
                                balance_401k,
                                current_contribution_401k,
                                match_percentage_401k,
                                portfolio_mix,
                                primary_card_interest_rate,
                                primary_card_debt,
                                secondary_card_interest_rate,
                                secondary_card_debt
                            )
            # Get the projections
            get_projections(calculator)
        # If there is an error
        except:
            # Display invalid input error
            st.error('Invalid Input', icon="🚨")
    else:
        # Display 401k contibution error message
        st.error('401k contribution cannot be higher than yearly savings.', icon="🚨")

# Display app title
st.write("# Financial Freedom")

# Create streamlit form
with st.form("Your Financials"):
    # Display for titel
    st.write("## Your Financials")

    # Get personal information
    st.write("### Personal Information")
    age = st.text_input("Age")

    # Get yearly income and savings information
    st.write("### Income/Savings")
    yearly_income = st.text_input("Yearly Income ($)")
    yearly_savings = st.text_input("Yearly Savings ($)")

    # Get 401k information
    st.write("### 401k")
    balance_401k = st.text_input("401k Balance ($)")
    current_contribution_401k = st.text_input("Current Contribution (%)")
    match_percentage_401k = st.text_input("Employer Match (%)")

    # Get Protfolio Mix information
    st.write("### Portfolio Mix")
    portfolio_mix = st.selectbox("Stocks/Bonds", ["20/80","40/60","60/40","80/20","100/0"])

    # Get credit card information
    st.write("### Credit Cards")
    st.write("##### Primary Card")
    primary_card_interest_rate = st.text_input("Primary Interest Rate (%)")
    primary_card_debt = st.text_input("Total Primary Debt ($)")
    st.write("##### Secondary Card")
    secondary_card_interest_rate = st.text_input("Secondary Interest Rate (%)")
    secondary_card_debt = st.text_input("Total Secondary Debt ($)")

    # If the form submit function is clicked
    if st.form_submit_button("Submit"):
        # Call the handle submittion function
        handle_submittion(
            age,yearly_income,
            yearly_savings,
            balance_401k,
            current_contribution_401k,
            match_percentage_401k,
            portfolio_mix,
            primary_card_interest_rate,
            primary_card_debt,
            secondary_card_interest_rate,
            secondary_card_debt
        )
