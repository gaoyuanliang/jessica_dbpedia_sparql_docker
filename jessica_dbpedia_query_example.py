from jessica_dbpedia_query import *

print(wikipage_id_to_dbpedia_id(wikipage_id = "5405"))
'''
http://dbpedia.org/resource/China
'''

print(find_entity_type("http://dbpedia.org/resource/China"))
'''
Country
'''

related_entity_triplets = find_related_entities(
	entity_id = "http://dbpedia.org/resource/Dubai",
	related_subject_num = 4,
	related_object_num = 4)

for t in related_entity_triplets:
	print(t)

'''
{'relation': 'http://dbpedia.org/ontology/campus', 'subject': 'http://dbpedia.org/resource/London_Business_School', 'object': 'http://dbpedia.org/resource/Dubai'}
{'relation': 'http://dbpedia.org/ontology/campus', 'subject': 'http://dbpedia.org/resource/Saint_Joseph_University', 'object': 'http://dbpedia.org/resource/Dubai'}
{'relation': 'http://dbpedia.org/ontology/birthPlace', 'subject': 'http://dbpedia.org/resource/Imad_Khalili', 'object': 'http://dbpedia.org/resource/Dubai'}
{'relation': 'http://dbpedia.org/ontology/deathPlace', 'subject': 'http://dbpedia.org/resource/Anisa_Makhlouf', 'object': 'http://dbpedia.org/resource/Dubai'}
{'relation': 'http://dbpedia.org/ontology/isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates', 'subject': 'http://dbpedia.org/resource/Dubai'}
{'relation': 'http://dbpedia.org/ontology/leaderName', 'object': 'http://dbpedia.org/resource/Mohammed_bin_Rashid_Al_Maktoum', 'subject': 'http://dbpedia.org/resource/Dubai'}
{'relation': 'http://dbpedia.org/ontology/leaderName', 'object': 'http://dbpedia.org/resource/Hamdan_bin_Mohammed_Al_Maktoum', 'subject': 'http://dbpedia.org/resource/Dubai'}
{'relation': 'http://dbpedia.org/ontology/governmentType', 'object': 'http://dbpedia.org/resource/Absolute_monarchy', 'subject': 'http://dbpedia.org/resource/Dubai'}
'''

pair_triplets = find_entity_pair_relation(
	entity_id_1 = "http://dbpedia.org/resource/Dubai", 
	entity_id_2 = "http://dbpedia.org/resource/Mohammed_bin_Rashid_Al_Maktoum",
	relation_1_to_2_number =4,
	relation_2_to_1_number = 4)

for t in pair_triplets:
	print(t)


'''
{'subject': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/leaderName', 'object': 'http://dbpedia.org/resource/Mohammed_bin_Rashid_Al_Maktoum'}
{'subject': 'http://dbpedia.org/resource/Mohammed_bin_Rashid_Al_Maktoum', 'relation': 'http://dbpedia.org/ontology/birthPlace', 'object': 'http://dbpedia.org/resource/Dubai'}
'''

linking_entity_triplets = find_linking_entities(
	entity_id_1 = "http://dbpedia.org/resource/Dubai",
	entity_id_2 = "http://dbpedia.org/resource/Abu_Dhabi",
	common_object_number = 3,
	common_subject_number = 3)

for t in linking_entity_triplets:
	print(t)

'''
{'subject': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/governmentType', 'object': 'http://dbpedia.org/resource/Absolute_monarchy'}
{'subject': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'http://dbpedia.org/ontology/governmentType', 'object': 'http://dbpedia.org/resource/Absolute_monarchy'}
{'subject': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates'}
{'subject': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'http://dbpedia.org/ontology/isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates'}
{'object': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/targetAirport', 'subject': 'http://dbpedia.org/resource/Pakistan_International_Airlines'}
{'object': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'http://dbpedia.org/ontology/targetAirport', 'subject': 'http://dbpedia.org/resource/Pakistan_International_Airlines'}
{'object': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/regionServed', 'subject': 'http://dbpedia.org/resource/Fakhro_Group'}
{'object': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'http://dbpedia.org/ontology/regionServed', 'subject': 'http://dbpedia.org/resource/Fakhro_Group'}
{'object': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/targetAirport', 'subject': 'http://dbpedia.org/resource/Airblue'}
{'object': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'http://dbpedia.org/ontology/targetAirport', 'subject': 'http://dbpedia.org/resource/Airblue'}
'''

output_triplets, entity_type_lookup, entity_name_lookup, relation_name_lookup = attach_triplet_type_and_name(related_entity_triplets+pair_triplets+linking_entity_triplets)

for t in output_triplets:
	print(t)

'''
{'relation': 'campus', 'subject': 'http://dbpedia.org/resource/London_Business_School', 'object': 'http://dbpedia.org/resource/Dubai', 'subject_type': 'University', 'object_type': 'City', 'subject_name': 'London Business School', 'object_name': 'Dubai'}
{'relation': 'campus', 'subject': 'http://dbpedia.org/resource/Saint_Joseph_University', 'object': 'http://dbpedia.org/resource/Dubai', 'subject_type': 'University', 'object_type': 'City', 'subject_name': 'Saint Joseph University', 'object_name': 'Dubai'}
{'relation': 'birthPlace', 'subject': 'http://dbpedia.org/resource/Imad_Khalili', 'object': 'http://dbpedia.org/resource/Dubai', 'subject_type': 'SoccerPlayer', 'object_type': 'City', 'subject_name': 'Imad Khalili', 'object_name': 'Dubai'}
{'relation': 'deathPlace', 'subject': 'http://dbpedia.org/resource/Anisa_Makhlouf', 'object': 'http://dbpedia.org/resource/Dubai', 'subject_type': 'OfficeHolder', 'object_type': 'City', 'subject_name': 'Anisa Makhlouf', 'object_name': 'Dubai'}
{'relation': 'isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates', 'subject': 'http://dbpedia.org/resource/Dubai', 'subject_type': 'City', 'object_type': 'Country', 'subject_name': 'Dubai', 'object_name': 'United Arab Emirates'}
{'relation': 'leaderName', 'object': 'http://dbpedia.org/resource/Mohammed_bin_Rashid_Al_Maktoum', 'subject': 'http://dbpedia.org/resource/Dubai', 'subject_type': 'City', 'object_type': 'Politician', 'subject_name': 'Dubai', 'object_name': 'Mohammed bin Rashid Al Maktoum'}
{'relation': 'leaderName', 'object': 'http://dbpedia.org/resource/Hamdan_bin_Mohammed_Al_Maktoum', 'subject': 'http://dbpedia.org/resource/Dubai', 'subject_type': 'City', 'object_type': 'Royalty', 'subject_name': 'Dubai', 'object_name': 'Hamdan bin Mohammed Al Maktoum'}
{'relation': 'governmentType', 'object': 'http://dbpedia.org/resource/Absolute_monarchy', 'subject': 'http://dbpedia.org/resource/Dubai', 'subject_type': 'City', 'object_type': 'Other', 'subject_name': 'Dubai', 'object_name': 'Absolute monarchy'}
{'subject': 'http://dbpedia.org/resource/Dubai', 'relation': 'leaderName', 'object': 'http://dbpedia.org/resource/Mohammed_bin_Rashid_Al_Maktoum', 'subject_type': 'City', 'object_type': 'Politician', 'subject_name': 'Dubai', 'object_name': 'Mohammed bin Rashid Al Maktoum'}
{'subject': 'http://dbpedia.org/resource/Mohammed_bin_Rashid_Al_Maktoum', 'relation': 'birthPlace', 'object': 'http://dbpedia.org/resource/Dubai', 'subject_type': 'Politician', 'object_type': 'City', 'subject_name': 'Mohammed bin Rashid Al Maktoum', 'object_name': 'Dubai'}
{'subject': 'http://dbpedia.org/resource/Dubai', 'relation': 'governmentType', 'object': 'http://dbpedia.org/resource/Absolute_monarchy', 'subject_type': 'City', 'object_type': 'Other', 'subject_name': 'Dubai', 'object_name': 'Absolute monarchy'}
{'subject': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'governmentType', 'object': 'http://dbpedia.org/resource/Absolute_monarchy', 'subject_type': 'City', 'object_type': 'Other', 'subject_name': 'Abu Dhabi', 'object_name': 'Absolute monarchy'}
{'subject': 'http://dbpedia.org/resource/Dubai', 'relation': 'isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates', 'subject_type': 'City', 'object_type': 'Country', 'subject_name': 'Dubai', 'object_name': 'United Arab Emirates'}
{'subject': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates', 'subject_type': 'City', 'object_type': 'Country', 'subject_name': 'Abu Dhabi', 'object_name': 'United Arab Emirates'}
{'object': 'http://dbpedia.org/resource/Dubai', 'relation': 'targetAirport', 'subject': 'http://dbpedia.org/resource/Pakistan_International_Airlines', 'subject_type': 'Airline', 'object_type': 'City', 'subject_name': 'Pakistan International Airlines', 'object_name': 'Dubai'}
{'object': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'targetAirport', 'subject': 'http://dbpedia.org/resource/Pakistan_International_Airlines', 'subject_type': 'Airline', 'object_type': 'City', 'subject_name': 'Pakistan International Airlines', 'object_name': 'Abu Dhabi'}
{'object': 'http://dbpedia.org/resource/Dubai', 'relation': 'regionServed', 'subject': 'http://dbpedia.org/resource/Fakhro_Group', 'subject_type': 'Company', 'object_type': 'City', 'subject_name': 'Fakhro Group', 'object_name': 'Dubai'}
{'object': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'regionServed', 'subject': 'http://dbpedia.org/resource/Fakhro_Group', 'subject_type': 'Company', 'object_type': 'City', 'subject_name': 'Fakhro Group', 'object_name': 'Abu Dhabi'}
{'object': 'http://dbpedia.org/resource/Dubai', 'relation': 'targetAirport', 'subject': 'http://dbpedia.org/resource/Airblue', 'subject_type': 'Airline', 'object_type': 'City', 'subject_name': 'Airblue', 'object_name': 'Dubai'}
{'object': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'targetAirport', 'subject': 'http://dbpedia.org/resource/Airblue', 'subject_type': 'Airline', 'object_type': 'City', 'subject_name': 'Airblue', 'object_name': 'Abu Dhabi'}
'''

print(entity_type_lookup)
'''
{'http://dbpedia.org/resource/United_Arab_Emirates': 'Country', 'http://dbpedia.org/resource/Abu_Dhabi': 'City', 'http://dbpedia.org/resource/Dubai': 'City', 'http://dbpedia.org/ontology/birthPlace': 'Other', 'http://dbpedia.org/resource/Absolute_monarchy': 'Other'}
'''

print(entity_name_lookup)
'''
{'http://dbpedia.org/resource/United_Arab_Emirates': 'United Arab Emirates', 'http://dbpedia.org/resource/Abu_Dhabi': 'Abu Dhabi', 'http://dbpedia.org/resource/Dubai': 'Dubai', 'http://dbpedia.org/ontology/birthPlace': 'birthPlace', 'http://dbpedia.org/resource/Absolute_monarchy': 'Absolute monarchy'}
'''
