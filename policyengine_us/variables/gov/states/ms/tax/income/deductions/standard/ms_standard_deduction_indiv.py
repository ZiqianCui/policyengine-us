from policyengine_us.model_api import *


class ms_standard_deduction_indiv(Variable):
    value_type = float
    entity = Person
    label = (
        "Mississippi standard deduction when married couples file separately"
    )
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.MS

    def formula(person, period, parameters):
        # First get the filing status.
        filing_status = person.tax_unit("filing_status", period)

        # Then get the MS Standard Deduction part of the parameter tree.
        p = parameters(period).gov.states.ms.tax.income.deductions.standard

        # Get their standard deduction amount based on their filing status.
        # Only the head will claim the standard deduction of the return is filed
        # separately on the same form
        is_head = person("is_tax_unit_head", period)
        return is_head * p.amount[filing_status]
