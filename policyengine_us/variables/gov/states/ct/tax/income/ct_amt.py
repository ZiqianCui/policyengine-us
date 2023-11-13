from policyengine_us.model_api import *


class ct_amt(Variable):
    value_type = float
    entity = TaxUnit
    label = "Connecticut alternative minimum tax"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.CT
    reference = (
        "https://portal.ct.gov/-/media/DRS/Forms/2022/Income/2022-CT-1040-Instructions_1222.pdf#page=2"  # line 9
        "https://portal.ct.gov/-/media/DRS/Forms/2022/Income/CT-1040_1222.pdf#page=1"  # line 9
        "https://portal.ct.gov/-/media/DRS/Forms/2022/Income/CT-6251_1222.pdf#page=1"  # line 23
    )

    def formula(tax_unit, period, parameters):
        # assign amt parameters
        p = parameters(period).gov.states.ct.tax.income
        amt = p.alternative_minimum_tax.rate

        ct_income_tax_recapture = tax_unit(
            "ct_income_tax_recapture", period
        )  # Line 20
        foreign_tax_credit = tax_unit("foreign_tax_credit", period)  # Line 13
        federal_minimum_tax = tax_unit(
            "alternative_minimum_tax", period
        )  # Line 14

        ct_minimum_tax = min_(
            foreign_tax_credit * amt.foreign_tax_credit_rate,  # Line 16
            federal_minimum_tax * amt.tentative_minimum_tax_rate,  # Line 15
        )  # Line 17

        return max_(ct_minimum_tax - ct_income_tax_recapture, 0)  # Line 21
