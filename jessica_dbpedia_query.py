#######jessica_dbpedia_query.py#######
import re
import rdflib

g_relation = rdflib.Graph()
g_type = rdflib.Graph()

print('loading the DBpedia knowledge base')

mappingbased_objects_en_small = g_relation.parse(
	"/jessica/mappingbased_objects_en_small.ttl", 
	format='ttl')
print(mappingbased_objects_en_small)

instance_types_en_small = g_type.parse(
	"/jessica/instance_types_en_small.ttl", 
	format='ttl')
print(instance_types_en_small)

print('knolwedge based loading completed.')

#######

def id_to_name(entity_id):
	entity_id = re.sub(r'^.*\/', r'',  entity_id)
	entity_id = re.sub(r'[^a-zA-Z\d\.]+', r' ', entity_id)
	return entity_id

def find_entity_type(entity_id):
	try:
		types = [t[1].toPython() for t in 
			g_type.query(u"""
			SELECT ?r ?o WHERE {
			<%s> ?r ?o .
			} LIMIT 1
			"""%(entity_id))]
		output = re.search(r'[^\/\\]+$', types[0]).group()
		output = re.sub(r'[^A-z]+', r'_', output)
		output = re.sub(r'^[^A-z]+|[^A-z]+$', r'', output)
		return output
	except:
		return 'Other'

'''
find_entity_type('http://dbpedia.org/resource/Kohn_Pedersen_Fox')
'''

def relation_processing(renaltion_name):
	output = re.sub(r'^.*\/', r'', renaltion_name)
	output = re.sub(r'[^A-z]+', r'_', output)
	output = re.sub(r'^[^A-z]+|[^A-z]+$', r'', output)
	return output

'''
print(relation_processing("http://dbpedia.org/ontology/ground"))
'''

def find_related_entities(
	entity_id,
	related_subject_num = 4,
	related_object_num = 4):
	objects = []
	subjects = []
	#####
	try:
		if related_object_num > 0:
			objects = [{'relation': stmt[0].toPython(), 
				'object':stmt[1].toPython(),
				'subject':entity_id}
				for stmt 
				in g_relation.query(u"""
				SELECT ?r ?o WHERE { <%s> ?r ?o . } LIMIT %d
				"""%(entity_id, related_object_num))]
	except:
		pass
	######
	try:
		if related_subject_num > 0:
			subjects = [{'relation': stmt[1].toPython(), 
				'subject':stmt[0].toPython(),
				'object':entity_id}
				for stmt 
				in g_relation.query(u"""
				SELECT ?s ?r WHERE { ?s ?r <%s>. } LIMIT %d
				"""%(entity_id, related_subject_num))]
	except:
		pass
	######
	return subjects+objects

'''
find_related_entities(
	entity_id = "http://dbpedia.org/resource/Dubai",
	related_subject_num = 1,
	related_object_num = 1)
'''

def find_linking_entities(
	entity_id_1, 
	entity_id_2,
	common_object_number,
	common_subject_number):
	output = []
	######
	try:
		for stmt in g_relation.query(u"""
			SELECT ?o ?r1 ?r2  WHERE { 
				<%s> ?r1 ?o . 
				<%s> ?r2 ?o . 
			} LIMIT %d
			"""%(entity_id_1, entity_id_2, common_object_number)):
			output.append({'subject':entity_id_1,
				'relation':stmt[1].toPython(),
				'object': stmt[0].toPython(), 
				})
			output.append({'subject':entity_id_2,
				'relation':stmt[2].toPython(),
				'object': stmt[0].toPython(), 
				})
	except:
		pass
	######
	try:
		for stmt in g_relation.query(u"""
			SELECT ?s ?r1 ?r2  WHERE { 
				?s ?r1 <%s> . 
				?s ?r2 <%s> . 
			} LIMIT %d
			"""%(entity_id_1, entity_id_2, common_subject_number)):
			output.append({'object':entity_id_1,
				'relation':stmt[1].toPython(),
				'subject': stmt[0].toPython(), 
				})
			output.append({'object':entity_id_2,
				'relation':stmt[2].toPython(),
				'subject': stmt[0].toPython(), 
				})
	except:
		pass
	#####
	return output

'''
find_linking_entities(
	entity_id_1 = "http://dbpedia.org/resource/Dubai",
	entity_id_2 = "http://dbpedia.org/resource/Abu_Dhabi",
	common_object_number = 1,
	common_subject_number = 1)
'''

def attach_triplet_type_and_name(input_triplets):
	entities = list(set([t['subject'] for t in input_triplets]+[t['object'] for t in input_triplets]))
	entity_type_lookup = {}
	entity_name_lookup = {}
	relation_name_lookup = {}
	outout_triplets = input_triplets
	for e in entities:
		entity_type_lookup[e] = find_entity_type(e)
		entity_name_lookup[e] = id_to_name(e)
	#######
	types = list(set([t['relation'] for t in input_triplets]))
	for t in types:
		relation_name_lookup[t] = relation_processing(t)
	######
	for t in outout_triplets:
		t['subject_type'] = entity_type_lookup[t['subject']]
		t['object_type'] = entity_type_lookup[t['object']]
		t['subject_name'] = entity_name_lookup[t['subject']]
		t['object_name'] = entity_name_lookup[t['object']]
		t['relation'] = relation_name_lookup[t['relation']]
	return outout_triplets, entity_type_lookup, entity_name_lookup, relation_name_lookup

'''
input_triplets = [{'subject': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates'}, {'subject': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'http://dbpedia.org/ontology/isPartOf', 'object': 'http://dbpedia.org/resource/United_Arab_Emirates'}, {'subject': 'http://dbpedia.org/resource/Dubai', 'relation': 'http://dbpedia.org/ontology/governmentType', 'object': 'http://dbpedia.org/resource/Absolute_monarchy'}, {'subject': 'http://dbpedia.org/resource/Abu_Dhabi', 'relation': 'http://dbpedia.org/ontology/governmentType', 'object': 'http://dbpedia.org/resource/Absolute_monarchy'}]
input_triplets, entity_type_lookup, entity_name_lookup = attach_triplet_type_and_name(input_triplets)
'''
#######jessica_dbpedia_query.py#######
