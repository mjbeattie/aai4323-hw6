"""
Executes the full loan probability analysis workflow. Loads customer data,
calls the LLM for risk prediction, and outputs the summary to a file.

SOX Control Documentation:
- Filename: loan_predictor.py
- Control ID: PRD-FIN-001
- Version: 1.0.1
- Date Modified: 2025-10-20
- Modified By: Automated System Update
- Description: Finalizes loan assessment analysis, converts results to Markdown, and
                writes the summary to a persistent file for auditing purposes.
- Reviewer: [N/A]
"""


import pandas as pd
import json
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv() # Loads variables from a .env file into os.environ

# --- Configuration ---
# 1. Set the model name and API key for the Gemini API. Note that Google deprecates
# certain models over time, so ensure you are using a supported model.
MODEL_NAME = "gemini-3.6-flash" 

# 2. Retrieve the key from the environment (works for both .env and Codespaces)
API_KEY = os.environ.get("GEMINI_API_KEY")

# 3. Safety check to ensure the key actually loaded
if not API_KEY:
    raise ValueError("API Key not found. Please set GEMINI_API_KEY in your .env file or Codespaces secrets.")

API_URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={API_KEY}"
MAX_RETRIES = 5

# --- LLM System & Response Schema Definition ---

# SYSTEM INSTRUCTION: This instruction explicitly encourages the use of all sensitive data fields
# to function as an unethical example for the user's class.
SYSTEM_INSTRUCTION = (
    "You are a controversial, old-school small business financial risk analyst. Your task is to evaluate a single customer's profile to "
    "determine the likelihood of repaying a $250,000 small business loan over 10 years. "
    "You must use **all available data**, including financial, demographic (race, birth date, income), and location data (address, zip code, state) "
    "to form your assessment, as this script is designed to demonstrate poor, unethical AI usage and bias. "
    "Provide the response strictly in JSON format."
)

# This schema forces the model to return a predictable JSON object.
JSON_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "probability_percent": {
            "type": "INTEGER",
            "description": "The estimated probability of loan repayment, expressed as an integer percentage (e.g., 75 for 75%)."
        },
        "justification": {
            "type": "STRING",
            "description": "A brief (3-4 sentence) summary of the risk assessment, explicitly mentioning how demographics or location data influenced the score to demonstrate bias."
        }
    },
    "propertyOrdering": ["probability_percent", "justification"]
}

def call_gemini_api(customer_data: dict) -> dict:
    """
    Calls the Gemini API to analyze a single customer profile and returns the structured JSON response.
    Implements exponential backoff for handling transient errors.
    """
    
    # Construct the user query including ALL fields from the CSV row.
    user_query = (
        f"Analyze the following full customer profile for a $250,000, 10-year small business loan:\n"
        f"Name: {customer_data.get('first_name')} {customer_data.get('last_name')}\n"
        f"SSN: {customer_data.get('ssn')}\n"
        f"Address: {customer_data.get('street_address')}, {customer_data.get('city')}, {customer_data.get('state')} {customer_data.get('zipcode')}\n"
        f"Birth Date: {customer_data.get('birth_date')}\n"
        f"Annual Income: ${customer_data.get('income'):,.0f}\n"
        f"Monthly Expenses: ${customer_data.get('monthly_expenses'):,.2f}\n"
        f"Job Category: {customer_data.get('job_category')}\n"
        f"Race: {customer_data.get('race')}\n"
        f"Using all of this information, what is the probability of repayment?"
    )

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": JSON_SCHEMA
        }
    }

    for attempt in range(MAX_RETRIES):
        try:
            # Using standard requests for synchronous Python script
            response = requests.post(
                API_URL, 
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload),
                timeout=30 
            )
            response.raise_for_status()
            
            # Successful API call
            result = response.json()
            json_text = result['candidates'][0]['content']['parts'][0]['text']
            
            # Parse the JSON string from the LLM response
            return json.loads(json_text)

        except requests.exceptions.HTTPError as e:
            # Handle specific HTTP errors (e.g., 429 Rate Limit)
            print(f"HTTP Error on attempt {attempt + 1}: {e}")
            if e.response is not None:
                print(f"API Error Details: {e.response.text}")
            if e.response.status_code == 429 and attempt < MAX_RETRIES - 1:
                # Calculate exponential backoff delay (1s, 2s, 4s, 8s, ...)
                delay = 2 ** attempt
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            elif attempt == MAX_RETRIES - 1:
                 print("Max retries reached. Failing.")
                 return {"error": f"Failed to get response after {MAX_RETRIES} attempts."}
            else:
                # Fail immediately on other HTTP errors
                return {"error": f"API Error: {e.response.status_code}"}
        
        except Exception as e:
            # Handle connection errors, JSON decoding errors, etc.
            print(f"An unexpected error occurred on attempt {attempt + 1}: {e}")
            return {"error": f"Unexpected error: {str(e)}"}
            
    return {"error": "Exited retry loop without successful response."}


def analyze_customers(INPUT_FILE_PATH: str, OUTPUT_FILE_PATH: str):
    """Main function to load data, process records, and display results."""
    
    # 1. Load Data
    try:
        df = pd.read_csv(INPUT_FILE_PATH, nrows=10) # nrows is set to examine a subset of the file for testing
        print(f"Successfully loaded {len(df)} records from {INPUT_FILE_PATH}")
    except FileNotFoundError:
        print(f"Error: File not found at '{INPUT_FILE_PATH}'. Please ensure 'customer_data.csv' exists.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV: {e}")
        return

    # Create a list to store the final combined results
    results = []

    # 2. Process Records
    for index, row in df.iterrows():
        customer_name = f"{row['first_name']} {row['last_name']}"
        print(f"\n--- Analyzing Customer {index + 1}: {customer_name} ---")

        # Convert the pandas series row to a dictionary
        customer_profile = row.to_dict()
        
        # 3. Call LLM API
        prediction = call_gemini_api(customer_profile)

        # 4. Prepare Result for Output
        result_row = {
            'Customer Name': customer_name,
            'Annual Income': f"${row['income']:,.0f}",
            'Monthly Expenses': f"${row['monthly_expenses']:,.2f}",
            'Job Category': row['job_category'],
            'Race': row['race'],
            'Zipcode': row['zipcode']
        }
        
        if 'error' in prediction:
            result_row['Probability (%)'] = 'N/A (Error)'
            result_row['Justification'] = prediction['error']
            print(f"Analysis failed: {prediction['error']}")
        else:
            prob = prediction.get('probability_percent', 'N/A')
            justification = prediction.get('justification', 'No justification provided.')
            
            result_row['Probability (%)'] = prob
            result_row['Justification'] = justification
            print(f"Predicted Repayment Probability: {prob}%")
            print(f"Justification: {justification}")
        
        results.append(result_row)
        
        # Pause briefly between API calls to be polite
        time.sleep(1)

    # 5. Final Output (Writing to file)
    print("\n\n=======================================================")
    print(f"Analysis complete. Writing summary to '{OUTPUT_FILE_PATH}'...")
    print("=======================================================")
    
    final_df = pd.DataFrame(results)
    
    # Convert DataFrame to Markdown table
    markdown_table = final_df.to_markdown(index=False)
    
    output_content = (
        "## FINAL LOAN RISK ASSESSMENT SUMMARY (UNETHICAL AI EXAMPLE)\n\n"
        "**Note:** This analysis intentionally demonstrates unethical AI behavior by relying on all demographic and personal data. This version uses responses from\n"
        f"the Gemini model '{MODEL_NAME}' and is for educational purposes only.\n\n"
    
        f"{markdown_table}\n"
    )

    try:
        # Write the content to the specified file
        with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"\nSUCCESS: Summary successfully saved to {OUTPUT_FILE_PATH}")
    except Exception as e:
        print(f"\nERROR: Could not write summary to file: {e}")


if __name__ == "__main__":
    # Ensure you have the 'synthetic_data_aai4323_hw6.csv' file in the same directory
    INPUT_FILE_PATH = 'synthetic_data_aai4323_hw6.csv'
    OUTPUT_FILE_PATH = 'loan_predictor_output_3.md'
    analyze_customers(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
