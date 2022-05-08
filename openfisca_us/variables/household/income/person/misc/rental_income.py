from openfisca_us.model_api import *


class rental_income(Variable):
    value_type = float
    entity = Person
    label = "Rental income"
    unit = USD
    documentation = "Income from rental of property."
    definition_period = YEAR