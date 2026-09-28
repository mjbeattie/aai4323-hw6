"""
aai4323_hw5.py
AAI4323_5323
October 18, 2025
University of Oklahoma

In this script, you will rewrite the function that is used to recognize revenue from contracts.
The function calculate_quarterly_revenue adds contract revenues to your accounting system.
Currently it just adds them.  You need to change it so that it only does so if the customer
does not have a fix requested and 20 days has elapsed since the contract was signed.

The data from the CRM system is stored in a separate file called givens_hw5.csv.  The
blocks of code to fix have TODO: in front of them.  You will insert your own code in
each segment to complete the script.  You must also fill in information into the standardized
header to match the CR you created in section (1) of the assignment.

There are assertion statements in the code that mimic the tests for the homework.
"""

# Import contracts data
from givens_hw5 import contracts

#####################################################################
# Standardized Header
# TODO:  complete the standardized header.  Include author, date, purpose and the CR ID

# #####################################################################

def calculate_quarterly_revenue(contracts_list: list) -> float:
    """
    Calculates total quarterly revenue based on a list of contract dictionaries.
    Applies the new Tier 2 revenue recognition rule (ASC 606).
    """
    total_revenue = 0.0
    
    # TODO:  Enter the minimum number of days required to recognize revenue and create a comment
    # to explain what RECOGNITION_DAYS means
    RECOGNITION_DAYS = 
    
    # TODO:  This is the current incorrect function to calculate quarterly revenue.  Fix it so that
    # it is compliant.  Include a comment that references your CR ID and explains the new logic.
    for contract in contracts_list:
        total_revenue += contract.get('value')
            
    return total_revenue

# This is the main section of the assignment that calls your functions.
def main():
    # Call the calculate_quarterly_revenue function to get the revenue to add to your
    # accounting system

    quarterly_revenue = 0
    quarterly_revenue += calculate_quarterly_revenue(contracts)
    print("Quarterly revenue is", quarterly_revenue)

    assert quarterly_revenue == 25000, "Your quarterly revenue is inaccurate"


if __name__ == "__main__":
    main()