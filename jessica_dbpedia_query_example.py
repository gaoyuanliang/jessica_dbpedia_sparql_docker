from jessica_dbpedia_query import *

related_entity_triplets = find_related_entities(
	entity_id = "http://dbpedia.org/resource/Dubai",
	related_subject_num = 1,
	related_object_num = 1)

for t in related_entity_triplets:
	print(t)

'''
{'relation': 'http://dbpedia.org/resource/Hamdan_bin_Rashid_Al_Maktoum', 'subject': 'http://dbpedia.org/ontology/birthPlace', 'object': 'http://dbpedia.org/resource/Dubai'}
{'relation': 'http://dbpedia.org/ontology/governmentType', 'object': 'http://dbpedia.org/resource/Absolute_monarchy', 'subject': 'http://dbpedia.org/resource/Dubai'}
'''

linking_entity_triplets = find_linking_entities(
	entity_id_1 = "http://dbpedia.org/resource/Dubai",
	entity_id_2 = "http://dbpedia.org/resource/Abu_Dhabi",
	common_object_number = 1,
	common_subject_number = 1)

for t in linking_entity_triplets:
	print(t)

'''
{'subject': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates'}
{'subject': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'http://dbpedia.org/ontology/isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates'}
{'object': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/largestCity', 'subject': 'http://dbpedia.org/resource/United_Arab_Emirates'}
{'object': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'http://dbpedia.org/ontology/capital', 'subject': 'http://dbpedia.org/resource/United_Arab_Emirates'}
'''

output_triplets, entity_type_lookup, entity_name_lookup = attach_triplet_type_and_name(related_entity_triplets+linking_entity_triplets)

for t in output_triplets:
	print(t)

'''
{'relation': 'http://dbpedia.org/resource/Hamdan_bin_Rashid_Al_Maktoum', 'subject': 'http://dbpedia.org/ontology/birthPlace', 'object': 'http://dbpedia.org/resource/Dubai', 'subject_type': 'Other', 'object_type': 'City', 'subject_name': 'birthPlace', 'object_name': 'Dubai'}
{'relation': 'http://dbpedia.org/ontology/governmentType', 'object': 'http://dbpedia.org/resource/Absolute_monarchy', 'subject': 'http://dbpedia.org/resource/Dubai', 'subject_type': 'City', 'object_type': 'Other', 'subject_name': 'Dubai', 'object_name': 'Absolute monarchy'}
{'subject': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates', 'subject_type': 'City', 'object_type': 'Country', 'subject_name': 'Dubai', 'object_name': 'United Arab Emirates'}
{'subject': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'http://dbpedia.org/ontology/isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates', 'subject_type': 'City', 'object_type': 'Country', 'subject_name': 'Abu Dhabi', 'object_name': 'United Arab Emirates'}
{'object': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/largestCity', 'subject': 'http://dbpedia.org/resource/United_Arab_Emirates', 'subject_type': 'Country', 'object_type': 'City', 'subject_name': 'United Arab Emirates', 'object_name': 'Dubai'}
{'object': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'http://dbpedia.org/ontology/capital', 'subject': 'http://dbpedia.org/resource/United_Arab_Emirates', 'subject_type': 'Country', 'object_type': 'City', 'subject_name': 'United Arab Emirates', 'object_name': 'Abu Dhabi'}
'''

print(entity_type_lookup)
'''
{'http://dbpedia.org/resource/United_Arab_Emirates': 'Country', 'http://dbpedia.org/resource/Abu_Dhabi': 'City', 'http://dbpedia.org/resource/Dubai': 'City', 'http://dbpedia.org/ontology/birthPlace': 'Other', 'http://dbpedia.org/resource/Absolute_monarchy': 'Other'}
'''

print(entity_name_lookup)
'''
{'http://dbpedia.org/resource/United_Arab_Emirates': 'United Arab Emirates', 'http://dbpedia.org/resource/Abu_Dhabi': 'Abu Dhabi', 'http://dbpedia.org/resource/Dubai': 'Dubai', 'http://dbpedia.org/ontology/birthPlace': 'birthPlace', 'http://dbpedia.org/resource/Absolute_monarchy': 'Absolute monarchy'}
'''
