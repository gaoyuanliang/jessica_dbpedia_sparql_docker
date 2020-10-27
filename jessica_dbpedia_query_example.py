from jessica_dbpedia_query import *

related_entity_triplets = find_related_entities(
	entity_id = "http://dbpedia.org/resource/Dubai",
	related_subject_num = 1,
	related_object_num = 1)

for t in related_entity_triplets:
	print(t)

linking_entity_triplets = find_linking_entities(
	entity_id_1 = "http://dbpedia.org/resource/Dubai",
	entity_id_2 = "http://dbpedia.org/resource/Abu_Dhabi",
	common_object_number = 1,
	common_subject_number = 1)

for t in linking_entity_triplets:
	print(t)

output_triplets, entity_type_lookup, entity_name_lookup = attach_triplet_type_and_name(related_entity_triplets+linking_entity_triplets)

for t in output_triplets:
	print(t)

print(entity_type_lookup)

print(entity_name_lookup)
