from policyengine_us.model_api import *


class regular_tax_before_credits(Variable):
    value_type = float
    entity = TaxUnit
    definition_period = YEAR
    label = "Regular tax before credits"
    documentation = "Regular tax on regular taxable income before credits"
    unit = USD

    def formula(tax_unit, period, parameters):
        capital_gains = parameters(period).gov.irs.capital_gains.brackets
        filing_status = tax_unit("filing_status", period)
        dwks1 = tax_unit("taxable_income", period)

        dwks16 = min_(capital_gains.thresholds["1"][filing_status], dwks1)
        dwks17 = min_(tax_unit("dwks14", period), dwks16)

        dwks20 = dwks16 - dwks17
        lowest_rate_tax = capital_gains.rates["1"] * dwks20
        # Break in worksheet lines
        dwks13 = tax_unit("dwks13", period)
        dwks21 = min_(dwks1, dwks13)
        dwks22 = dwks20
        dwks23 = max_(0, dwks21 - dwks22)
        dwks25 = min_(capital_gains.thresholds["2"][filing_status], dwks1)
        dwks19 = tax_unit("dwks19", period)
        dwks26 = min_(dwks19, dwks20)
        dwks27 = max_(0, dwks25 - dwks26)
        dwks28 = min_(dwks23, dwks27)
        dwks29 = capital_gains.rates["2"] * dwks28
        dwks30 = dwks22 + dwks28
        dwks31 = dwks21 - dwks30
        dwks32 = capital_gains.rates["3"] * dwks31
        # Break in worksheet lines
        dwks33 = min_(
            tax_unit("dwks9", period),
            add(tax_unit, period, ["unrecaptured_section_1250_gain"]),
        )
        dwks10 = tax_unit("dwks10", period)
        dwks34 = dwks10 + dwks19
        dwks36 = max_(0, dwks34 - dwks1)
        dwks37 = max_(0, dwks33 - dwks36)
        dwks38 = 0.25 * dwks37
        # Break in worksheet lines
        dwks39 = dwks19 + dwks20 + dwks28 + dwks31 + dwks37
        dwks40 = dwks1 - dwks39
        dwks41 = 0.28 * dwks40

        # SchXYZ call in Tax-Calculator

        reg_taxinc = max_(0, dwks19)

        # Initialise regular income tax to zero
        reg_tax = 0
        last_reg_threshold = 0
        individual_income = parameters(period).gov.irs.income
        for i in range(1, 7):
            # Calculate rate applied to regular income up to the current
            # threshold (on income above the last threshold)
            reg_threshold = individual_income.bracket.thresholds[str(i)][
                filing_status
            ]
            amount_in_bracket = amount_between(
                reg_taxinc, last_reg_threshold, reg_threshold
            )
            reg_tax += (
                individual_income.bracket.rates[str(i)] * amount_in_bracket
            )
            last_reg_threshold = reg_threshold

        # Calculate regular tax above the last threshold
        reg_tax += individual_income.bracket.rates["7"] * max_(
            reg_taxinc - last_reg_threshold, 0
        )

        dwks42 = reg_tax

        dwks43 = sum(
            [
                dwks29,
                dwks32,
                dwks38,
                dwks41,
                dwks42,
                lowest_rate_tax,
            ]
        )
        c05200 = tax_unit("income_tax_main_rates", period)
        dwks44 = c05200
        dwks45 = min_(dwks43, dwks44)

        hasqdivltcg = tax_unit("hasqdivltcg", period)

        return where(hasqdivltcg, dwks45, c05200)


taxbc = variable_alias("taxbc", regular_tax_before_credits)
