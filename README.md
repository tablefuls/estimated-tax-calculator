# Estimated Tax Calculator

This Estimated Tax Calculator is a Python script designed to help individuals
estimate their tax payments in the United States based on the IRS guidelines.
By inputting relevant financial information such as tax withholdings and
previous tax year data, the script calculates the estimated tax payments due
for each due date, helping taxpayers avoid underpayment penalties.

## Disclaimer

This program offers estimations based on the author's understanding of tax
guidelines and is not legal or professional advice. Tax regulations can change,
and this tool might not address all specifics of your situation. For detailed
and personalized advice, consult a qualified tax professional.

## Motivation

Calculating estimated tax payments can often be straightforward when all
pertinent information is readily available. For instance, Form 2210 outlines a
scenario where the total estimated tax payment is directly tied to the previous
year's tax amount and the anticipated tax withholdings for the current year.
The tax amount for the previous year is known upon completion of the tax
return, and for many, the upcoming year's tax withholding can be reasonably
estimated with Form W-4.

Navigating tax calculations grows intricate as withholdings accrue
incrementally throughout the year, while estimated tax payments must be made at
specific intervals and cannot be retroactively adjusted. To ensure accuracy and
avoid underpayment penalties, it's more prudent to base calculations on actual
amounts withheld up to each due date, rather than relying on projected annual
totals. This dynamic introduces two primary challenges:

1. Variability in tax withholdings by each due date.
2. Potential overpayments for previous periods due to increasing withholdings
   over time, necessitating adjustments in subsequent periods.

With each adjustment in withholding or payment strategy, there's a need to
reassess the estimated payments for upcoming due dates. This program is
designed to tackle these challenges, streamlining the process and offering a
user-friendly solution for tax payment estimation.

## Installation

This Python script is self-contained in a single file. Simply copy the script's
content and run it in an online Python playground for easy execution.

## Usage

1. Run the script and follow the prompts to input your financial data.
2. The script will then calculate the estimated tax payments by each due date
   based on the provided information.
3. Review the estimation output to ensure accuracy and compliance with IRS
   guidelines.
4. Make adjustments to your estimated payments as necessary.

## License

This project is licensed under the [MIT License](./LICENSE).
