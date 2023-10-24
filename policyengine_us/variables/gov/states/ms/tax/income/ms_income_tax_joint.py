from policyengine_us.model_api import *


class ms_income_tax_joint(Variable):
    value_type = float
    entity = Person
    label = "Mississippi income tax filing jointly"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.MS

    def formula(person, period, parameters):
        before_non_refundable_credits = person(
            "ms_income_tax_before_credits_joint", period
        )
        non_refundable_credits = person("ms_non_refundable_credits", period)
        return max_(before_non_refundable_credits - non_refundable_credits, 0)
