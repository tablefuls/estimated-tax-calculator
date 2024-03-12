from datetime import date
from typing import Final

# *****************************************************************************
# Inputs
# *****************************************************************************

this_year = date.today().year
this_year = int(
    input("The current tax year (default: {}): ".format(this_year)).strip()
    or this_year
)

prev_year = this_year - 1

next_year = this_year + 1

# To avoid penalties for a given year, the combined withholding and timely
# estimated tax payments should at least equal the lesser of:
#
# 1. 90% of the tax due for the current year, or
# 2. 100% of the tax from the previous year, ensuring the tax return spans a
#    12-month period. For higher-income taxpayers, this threshold increases to
#    110%.
#
# Case 1 can be challenging to predict, as it depends on the current year's tax
# liability, which might not be fully known until the year ends. In contrast,
# case 2 is more straightforward since it relies on the already determined tax
# from the previous year. This program primarily addresses case 2.
#
prev_year_tax = int(
    input(
        "The tax from the {} tax year (default: 0): ".format(prev_year)
    ).strip()
    or 0
)

prev_year_percent = int(
    input(
        "The percentage of tax for the {} tax year \
(100 or 110, default: 110): ".format(
            prev_year
        )
    ).strip()
    or 110
)

this_year_required_tax = round(prev_year_tax * prev_year_percent / 100)

this_year_withheld_tax = round(
    float(
        input(
            "The federal income tax withheld for the {} tax year \
(default: 0): ".format(
                this_year
            )
        ).strip()
        or 0
    )
)

PERIODS: Final[int] = 4

this_year_estimated_tax_due_dates = [
    date(this_year, 4, 15).strftime("%m/%d/%Y"),
    date(this_year, 6, 15).strftime("%m/%d/%Y"),
    date(this_year, 9, 15).strftime("%m/%d/%Y"),
    date(next_year, 1, 15).strftime("%m/%d/%Y"),
]

assert len(this_year_estimated_tax_due_dates) == PERIODS

this_year_estimated_tax_least_payments = [
    # NOTE: When filling out Form 2210 where lines 10 (required installment)
    # and 11 (estimated tax paid and tax withheld) represent two separate
    # values, it's best to write the formula to match these lines directly,
    # rather than relying on other calculations such as below to avoid
    # potential subtle differences.
    #
    # ```
    # round((this_year_required_tax - this_year_withheld_tax) / PERIODS)
    # ```
    #
    round(this_year_required_tax / PERIODS)
    - round(this_year_withheld_tax / PERIODS)
] * PERIODS

# The payment by each due date may be calculated by this program or input
# manually. If a payment has already been made, it should be entered to
# facilitate the calculation of remaining payments. The amount entered can
# exceed but should not fall below the program’s calculation. When a payment
# amount is left as "TBD", the program will automatically calculate its value.
#
TBD: Final[int] = -1

this_year_estimated_tax_actual_payments = [TBD] * PERIODS

for i, due_date in enumerate(this_year_estimated_tax_due_dates):
    this_year_estimated_tax_actual_payments[i] = int(
        input(
            "The estimated tax amount paid by the due date of {} \
(default: TBD): ".format(
                due_date
            )
        ).strip()
        or TBD
    )

    # To simplify the algorithm, the payment for each due date is determined
    # sequentially. An undetermined payment for a specific period implies that
    # subsequent payments also require calculation. This sequential logic is in
    # line with the fact that the amount due on each due date depends on the
    # sum of previous payments.
    #
    if this_year_estimated_tax_actual_payments[i] == TBD:
        break

# *****************************************************************************
# Estimation
# *****************************************************************************

for i, payment in enumerate(this_year_estimated_tax_actual_payments):
    if payment == TBD:
        carryover = sum(this_year_estimated_tax_actual_payments[0:i]) - sum(
            this_year_estimated_tax_least_payments[0:i]
        )

        payment = this_year_estimated_tax_least_payments[i] - carryover

        this_year_estimated_tax_actual_payments[i] = (
            payment if payment > 0 else 0
        )

print("\nEstimated tax payments:")
print("=" * 59)
print(
    "  {:^10}  |  {:^10}  |  {:^10}  |  {:^10}  ".format(
        *this_year_estimated_tax_due_dates
    )
)
print("=" * 59)
print(
    "  {:>10}  |  {:>10}  |  {:>10}  |  {:>10}  ".format(
        *this_year_estimated_tax_actual_payments
    )
)
print("-" * 59)

# *****************************************************************************
# Verification
# *****************************************************************************

lines = [[0] * PERIODS for i in range(19)]

for i in range(PERIODS):
    # Line 10: Required installment.
    #
    lines[10][i] = round(this_year_required_tax / PERIODS)

    # Line 11: Estimated tax paid and tax withheld.
    #
    lines[11][i] = this_year_estimated_tax_actual_payments[i] + round(
        this_year_withheld_tax / PERIODS
    )

    # Line 12: Accumulated overpayment from previous periods.
    #
    # This line accounts for the accumulated overpayment from all preceding
    # periods, if any. It specifically refers to the amount recorded on line 18
    # (overpayment) of the previous period.
    #
    lines[12][i] = lines[18][i - 1] if i > 0 else "N/A"

    # Line 13: Total payment available by current due date
    #
    # This line represents the total amount available for payment by the
    # current due date. It is the sum of lines 11 (estimated tax paid and tax
    # withheld) and 12 (accumulated overpayment from previous periods).
    #
    lines[13][i] = (lines[11][i] + lines[12][i]) if i > 0 else "N/A"

    # Line 14: Accumulated underpayment from previous periods.
    #
    # This line accounts for the accumulated underpayment from all preceding
    # periods, if any. It's the sum of lines 16 (insufficiency due to prior
    # underpayments) and 17 (underpayment) from the previous period.
    #
    # Line 16 is necessary in addition to line 17. While an underpayment
    # indicated in line 17 never exceeds the required installment for that
    # period (due to line 15 always being equal to or greater than zero), the
    # actual accumulated underpayment could surpass it. Since line 16 is
    # calculated as the reversal of the negative value obtained during the
    # computation of line 15, including it provides a comprehensive view of the
    # actual accumulated underpayment.
    #
    lines[14][i] = (
        ((lines[16][i] if lines[16][i] != "N/A" else 0) + lines[17][i])
        if i > 0
        else "N/A"
    )

    # Line 15: Net balance
    #
    # This line represents the net balance for the current period after
    # adjusting for any underpayment or overpayment carried forward from
    # previous periods with the current period's total payment available. It's
    # calculated by subtracting line 13 (total payment available by the current
    # due date) from line 14 (accumulated underpayment from previous periods).
    # If the result is zero or negative, enter 0. For the first period, where
    # there's no prior underpayment or overpayment, the balance will simply
    # equal the tax paid for this period (line 11).
    #
    # NOTE: Line 15 never has negative values. It seems to follow the logic
    # that an underpayment shown in line 17 (underpayment) shouldn't exceed the
    # required installment.
    #
    lines[15][i] = (lines[13][i] - lines[14][i]) if i > 0 else lines[11][i]
    if lines[15][i] < 0:
        lines[15][i] = 0

    # Line 16: Insufficiency due to prior underpayments.
    #
    # This line is only relevant in scenarios where line 15 indicates an
    # insufficiency. It quantifies the deficit amount that must be carried
    # forward to subsequent due dates. In essence, line 16 is calculated by
    # reversing the negative value obtained during the computation of line 15.
    #
    if i == 0 or i == PERIODS - 1:
        lines[16][i] = "N/A"
    elif lines[15][i] == 0:
        lines[16][i] = lines[14][i] - lines[13][i]

    # Line 17: Underpayment.
    #
    # Line 18: Overpayment.
    #
    # These two lines indicate whether there's an underpayment or overpayment
    # by the current due date. They are calculated based on the difference
    # between the amount on line 10 (required installment) and the value on
    # line 15 (net balance).
    #
    if lines[10][i] >= lines[15][i]:
        lines[17][i] = lines[10][i] - lines[15][i]
    else:
        lines[18][i] = lines[15][i] - lines[10][i]

print("\nVerfication with Form 2210 Part III Penalty Computation:")
print("=" * 74)
print(
    "  {:10}  |  {:^10}  |  {:^10}  |  {:^10}  |  {:^10}  ".format(
        "", *this_year_estimated_tax_due_dates
    )
)
print("=" * 74)
for i in range(10, 19):
    print(
        "  {:^10}  |  {:>10}  |  {:>10}  |  {:>10}  |  {:>10}  ".format(
            "Line {:2}".format(i), *lines[i]
        )
    )
    print("-" * 74)
