from tilt import tilt

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
    exists=False,
    reasoning="No legitimate interests"
)

non_disclosure = tilt.NonDisclosure(
    legal_requirement=False,
    contractual_regulation=False,
    obligation_to_provide=False,
    consequences="If the data is not disclosed, the shipment cannot be delivered."
)

purposes = tilt.AnyOfSchemaForThePurposes( 
    purpose="To provide the user-service-tilt",
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
first_disclosed_data = tilt.DataDisclosedElement(
    id='user-service-tilt-01',
    category="Language Preference",
    legal_bases=[first_legal_base, second_legal_base],
    storage=[storage],
    legitimate_interests=[legitimate_interests],
    non_disclosure=non_disclosure,
    purposes=[purposes],
    recipients=[first_recipient]
)

data_disclosed=[first_disclosed_data.to_dict()]

tilt_dict = {}
tilt_dict['dataDisclosed'] = data_disclosed

# with open('user_service_tilt.json', 'w') as fp:
#     json.dump(tilt_dict, fp, indent=4)
