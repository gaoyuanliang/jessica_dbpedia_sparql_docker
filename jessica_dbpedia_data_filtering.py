#############jessica_dbpedia_data_filtering.py#######
'''
https://github.com/tyrex-team/sparqlgx

RUN wget http://downloads.dbpedia.org/2016-10/core-i18n/en/mappingbased_objects_en.ttl.bz2
RUN bzip2 -d mappingbased_objects_en.ttl.bz2

RUN wget http://downloads.dbpedia.org/2016-10/core-i18n/en/instance_types_en.ttl.bz2
RUN bzip2 -d instance_types_en.ttl.bz2

https://wiki.dbpedia.org/downloads-2016-10

'''

import csv
import pandas
from pyspark import *
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *

sc = SparkContext("local")
sqlContext = SparkSession.builder.getOrCreate()

'''
load the data
'''
print('loading the data')

schema = StructType()\
	.add("subject",StringType(),True)\
	.add("relation",StringType(),True)\
	.add("object",StringType(),True)

out_degree_en = sqlContext.read.format('csv')\
	.options(delimiter=' ')\
	.schema(schema)\
	.load('/jessica/out_degree_en.ttl')
out_degree_en.registerTempTable('out_degree_en')

def extract_outdegree(input):
	try:
		input = input.strip()
		outdegree = re.search(r'\"(?P<outdegree>\d+)\"\^\^', input).group('outdegree')
		outdegree = int(outdegree)
		return outdegree
	except:
		return None

udf_extract_outdegree = udf(extract_outdegree, IntegerType())

out_degree_en.withColumn('outdegree', udf_extract_outdegree('object')).write.mode("Overwrite").json("/jessica/out_degree_en1")
sqlContext.read.json("/jessica/out_degree_en1").registerTempTable("out_degree_en1")

sqlContext.sql(u"""
	SELECT *, ROW_NUMBER() OVER ( ORDER BY outdegree DESC ) AS outdegree_rank
	FROM out_degree_en1
	""").write.mode("Overwrite").json("/jessica/out_degree_en2")
sqlContext.read.json("/jessica/out_degree_en2").registerTempTable("out_degree_en2")

'''
2274166
3660637
4780541
100000
'''

sqlContext.sql(u"""
	SELECT * FROM out_degree_en2 WHERE outdegree_rank <= 500000
	""").write.mode("Overwrite").json("/jessica/out_degree_en_small")
sqlContext.read.json("/jessica/out_degree_en_small").registerTempTable("out_degree_en_small")

########relation

mappingbased_objects_en = sqlContext.read.format('csv')\
	.options(delimiter=' ')\
	.schema(schema)\
	.load('/jessica/mappingbased_objects_en.ttl')
mappingbased_objects_en.registerTempTable('mappingbased_objects_en')

sqlContext.sql(u"""
	SELECT *
	FROM mappingbased_objects_en
	WHERE relation LIKE "%dbpedia%org%ontology%"
	""").write.mode("Overwrite").json("/jessica/mappingbased_objects_en1")
sqlContext.read.json("/jessica/mappingbased_objects_en1").registerTempTable("mappingbased_objects_en1")

######type

instance_types_en = sqlContext.read.format('csv')\
	.options(delimiter=' ')\
	.schema(schema)\
	.load('/jessica/instance_types_en.ttl')
instance_types_en.registerTempTable('instance_types_en')

sqlContext.sql(u"""
	SELECT *
	FROM instance_types_en
	WHERE object LIKE "%dbpedia%org%ontology%"
	""").write.mode("Overwrite").json("/jessica/instance_types_en1")
sqlContext.read.json("/jessica/instance_types_en1").registerTempTable("instance_types_en1")

####wikipage id

page_ids_en = sqlContext.read.format('csv')\
	.options(delimiter=' ')\
	.schema(schema)\
	.load('/jessica/page_ids_en.ttl')
page_ids_en.registerTempTable('page_ids_en')

######merget type and pageid to one table

sqlContext.sql(u"""
	SELECT out_degree_en_small.*,
	instance_types_en1.relation AS type_relation, 
	instance_types_en1.object AS type_object
	FROM out_degree_en_small
	LEFT JOIN instance_types_en1
	ON instance_types_en1.subject = out_degree_en_small.subject
	""").write.mode("Overwrite").json("temp1")
sqlContext.read.json("temp1").registerTempTable("temp1")

sqlContext.sql(u"""
	SELECT temp1.*,
	page_ids_en.relation AS wikipage_relation, 
	page_ids_en.object AS wikipage_object
	FROM temp1
	LEFT JOIN page_ids_en 
	ON page_ids_en.subject = temp1.subject
	""").write.mode("Overwrite").json("/jessica/entity_type_wikipage_small")
sqlContext.read.json("/jessica/entity_type_wikipage_small").registerTempTable("entity_type_wikipage_small")

sqlContext.sql(u"""
	SELECT 
	CASE 
		WHEN type_relation IS NOT NULL AND type_object IS NOT NULL 
		THEN 
		CONCAT(subject, ' ', relation, ' ', object, ' ; ',
		type_relation, ' ', type_object, ' ; ',
		wikipage_relation, ' ', wikipage_object, ' . ')
		ELSE 
		CONCAT(subject, ' ', relation, ' ', object, ' ; ',
		wikipage_relation, ' ', wikipage_object, ' . ')
	END
	FROM entity_type_wikipage_small
	WHERE wikipage_object IS NOT NULL
	""").write.mode("Overwrite").format("text").save("/jessica/entity_type_wikipage_small1")

'''
cat entity_type_wikipage_small1/* > entity_type_wikipage_small.ttl
'''

########save the relation to one table

sqlContext.sql(u"""
	SELECT mappingbased_objects_en1.* 
	FROM mappingbased_objects_en1
	JOIN out_degree_en_small
	ON out_degree_en_small.subject = mappingbased_objects_en1.subject
	""").write.mode("Overwrite").json("temp1")
sqlContext.read.json("temp1").registerTempTable("temp1")
sqlContext.sql(u"""
	SELECT temp1.*
	FROM temp1
	JOIN out_degree_en_small
	ON out_degree_en_small.subject = temp1.object
	""").write.mode("Overwrite").json("/jessica/mappingbased_objects_en_small")
sqlContext.read.json("/jessica/mappingbased_objects_en_small").registerTempTable("mappingbased_objects_en_small")

sqlContext.sql(u"""
	SELECT DISTINCT 
	CONCAT(subject, ' ', relation, ' ', object, ' . ')
	FROM mappingbased_objects_en_small
	""").write.mode("Overwrite").format("text").save("/jessica/mappingbased_objects_en_small1")

'''
cat mappingbased_objects_en_small1/* > mappingbased_objects_en_small.ttl
cat mappingbased_objects_en_small/* | wc -l 
1294722
'''

'''
test
'''
import os
import time
import rdflib

start_time = time.time()
g = rdflib.Graph()
g.parse("/jessica/entity_type_wikipage_small.ttl", format='ttl')
print('loading time:\t %f'%(time.time()-start_time))

entities = [(t[0].toPython(), t[1].toPython(), t[2].toPython()) for t in 
	g.query(u"""
	SELECT ?entity ?wikipage ?type
	WHERE { 
	?entity <http://dbpedia.org/ontology/wikiPageID> ?wikipage .
	?entity <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?type .
	} LIMIT 10
	""")]

for e in entities:
	try:
		print(e)
	except:
		pass

start_time = time.time()
g1 = rdflib.Graph()
g1.parse("/jessica/mappingbased_objects_en_small.ttl", format='ttl')
print('loading time:\t %f'%(time.time()-start_time))
#loading time:	 245.068069

relations = [(t[0].toPython(), t[1].toPython(), t[2].toPython()) for t in 
	g1.query(u"""
	SELECT ?s ?r ?o
	WHERE { ?s ?r ?o } LIMIT 10
	""")]

for r in relations:
	print(r)

#############jessica_dbpedia_data_filtering.py#######
