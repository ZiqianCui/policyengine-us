from policyengine_us.model_api import *


class ms_income_tax_indiv(Variable):
    value_type = float
    entity = TaxUnit
    label = "Mississippi income tax filing seperately"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.MS

    def formula(tax_unit, period, parameters):
        before_non_refundable_credits = tax_unit(
            "ms_income_tax_before_credits_indiv", period
        )
        non_refundable_credits = tax_unit("ms_non_refundable_credits", period)
        return max_(before_non_refundable_credits - non_refundable_credits, 0)
