# AAI and DSAI 4323/5323 HW6
## University of Oklahoma

This repository contains the files required to complete the coding part of
assignment six in AAI4323/5323 and DSAI4323/5323. Once you've created
your own repository from the template, you can launch a codespace to complete
the assignment.

You just started working for a bank that issues small business loans to applicants. You
are replacing an analyst who mysteriously quit and has disappeared, and you’ve been
asked to review her code. You are working on a Python script that uses a call to
Google’s Gemini LLM to predict whether loan applicants are likely to payback a
$250,000 loan over ten years. Your bank can issue these loans in the EU, U.S. and
China.

Because you know something about privacy, bias, and AI regulation, you must review
the code and make recommendations for how to comply with regulations in each area.
There are files included in the assignment for you:
+ _synthetic_data_aai4323_hw6.csv_: this is a CSV file containing a list of 100
applicants for loans.
+ _loan_predictor.py_: this is a Python script that generates predictions of the
applicants’ ability to pay back the loan. This is a script you can run if you would
like to. To do that, you will need to install the necessary packages used in the
include statements into a conda environment. You will also need an API Key
from Google AI Studio. It is free to use the Gemini API for small scale
applications and testing. I encourage you to try it. You will put your API key into
the .env file. However, you do not need to run the code to complete this
assignment.
+ _loan_predictor_output.md_: this is a markdown file that contains the output for
10 of the applicants. You’ll see that in several cases it points out that the zip
codes don’t match the cities. This is because the synthetic data ignores proper
city to zip code matching. Focus instead on the reasons for approval or denial
based on other factors.

1. In a few sentences, describe what this code does. Think about what it takes for inputs,
what it creates as output, and what algorithm, methods, or services it uses to generate
that output. (20 points)
2. In what region(s) would this code adhere to regulations as written? (5 points)
3. What is the EU risk classification for this program? (5 points)
4. As written, is the algorithm explainable? Why or why not? (20 points)
5. How would you add human oversight to the loan approval process to adhere to EU and
China regulations? (20 points)
6. The code is well commented. What document would you need to include with the code
if audited to conform to SOX and the EU AI Act? (5 points)
7. The U.S. Department of Justice (DOJ) has pursued cases where AI systems or
algorithmic scoring violates civil rights (for example race-based discrimination). Does
this code put your company at risk of being found guilty of civil rights violations? If so,
why? And if so, how can you fix the code? (25 points)

Save the answers to the questions above in a PDF with the naming convention
_aai4323_hw6_\_\<_your OU ID_\>._pdf_. Then upload this file to the Canvas assignment page.
