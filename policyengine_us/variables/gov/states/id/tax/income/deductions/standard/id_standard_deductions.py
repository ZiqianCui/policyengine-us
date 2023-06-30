from policyengine_us.model_api import *


class id_standard_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "Idaho standard deduction"
    unit = USD
    documentation = "https://tax.idaho.gov/wp-content/uploads/forms/EIS00407/EIS00407_01-05-2023.pdf"
    definition_period = YEAR
    defined_for = StateCode.ID

    def formula(tax_unit, period, parameters):
        person = tax_unit.members
        head = person("is_tax_unit_head", period)
        p = parameters(period).gov.states.id.tax.income.deductions.standard
        filing_status = tax_unit("filing_status", period)
        # base standard deduction amount
        base_amt = p.amount[filing_status]
        # check if filer can be claimed as a dependent
        is_dependent = person("is_tax_unit_dependent", period)
        # earned income calculation
        earned_income = person("earned_income", period)
        dependet_earned_income = tax_unit.any(is_dependent * earned_income)
        earned_income_amount = where(
            dependet_earned_income < p.dependents.income_threshold,
            p.dependents.min_amount,
            dependet_earned_income + p.dependents.addition,
        )
        # if dependent calculation
        dependent_amount = where(
            tax_unit.any(head & is_dependent),
            min_(base_amt, earned_income_amount),
            base_amt,
        )
        # Blind or aged deduction
        blind_head = tax_unit("blind_head", period).astype(int)
        blind_spouse = tax_unit("blind_spouse", period).astype(int)
        age_threshold = p.old_age_eligibility
        aged_head = (tax_unit("age_head", period) >= age_threshold).astype(int)
        aged_spouse = (tax_unit("age_spouse", period) >= age_threshold).astype(
            int
        )
        aged_blind_count = blind_head + blind_spouse + aged_head + aged_spouse
        extra_amt = aged_blind_count * p.additions[filing_status]
        return dependent_amount + extra_amt
