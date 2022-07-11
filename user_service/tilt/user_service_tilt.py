from tilt import tilt
import fastjsonschema
import json
import requests

#List of legal_bases with reference and description
first_legal_base = tilt.AnyOfSchemaForTheLegalBasesOfTheDataDisclosed(
    reference="GDPR-99-1-a",
    description="General Data Protection Regulation (GDPR) Art."
)
second_legal_base = tilt.AnyOfSchemaForTheLegalBasesOfTheDataDisclosed(
    reference="BDSG-42-5",
    description="BDSG-42-5 refers to the processing of personal data within.."
)

#Store the user-service-tilt
temporal = tilt.TemporalElement(
    description='Temporal element for the user-service-tilt',
    ttl=''
)
storage = tilt.StorageElement(
    temporal=[temporal], 
    purpose_conditional=["Data is always stored"],
    legal_basis_conditional=["SGB-100-42"],
    aggregation_function=tilt.AggregationFunction.MIN
    )

legitimate_interests = tilt.AnyOfSchemaForLegitimateInterests(
    exists=True,
    reasoning="No legitimate interests"
)

non_disclosure = tilt.NonDisclosure(
    legal_requirement=False,
    contractual_regulation=False,
    obligation_to_provide=False,
    consequences="If the data is not disclosed, the shipment cannot be delivered."
)

purposes1 = tilt.AnyOfSchemaForThePurposes( 
    purpose="To store the user's preferences and notification settings",
    description="To provide the user-service-tilt"
)

purposes2 = tilt.AnyOfSchemaForThePurposes( 
    purpose="Sending push notifications with information",
    description="To provide the user-service-tilt"
)

first_recipient = tilt.Recipient(
    name="",
    address="",
    category="",
    country="DE",
    division="",
    representative=None
)

#Data disclosed to user-service-tilt
disclosed_data = tilt.DataDisclosedElement(
    id='user-service-tilt-01',
    category="Language Preference",
    legal_bases=[first_legal_base, second_legal_base],
    storage=[storage],
    legitimate_interests=[legitimate_interests],
    non_disclosure=non_disclosure,
    purposes=[purposes1, purposes2],
    recipients=[first_recipient]
)

tilt_dict = {}
tilt_dict['dataDisclosed'] = [disclosed_data.to_dict()]

#Add validator to check the tilt_dict
# Load schema to validate against
file = requests.get('https://raw.githubusercontent.com/Transparency-Information-Language/schema/master/tilt-schema.json')
schema = json.loads(file.content)

#As we don't use the full TILT spec, we only need the 'dataDisclosed' schema from the file
examples_schema = schema['examples']
dataDisclosed_schema = examples_schema[0]['dataDisclosed']
# Compile schema
validate_func = fastjsonschema.compile(dataDisclosed_schema[0])

# Validate instance against schema
validate_func(tilt_dict)
