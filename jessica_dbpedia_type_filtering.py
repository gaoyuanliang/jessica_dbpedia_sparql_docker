#############jessica_dbpedia_type_filtering.py#############
'''
https://github.com/tyrex-team/sparqlgx
'''

import csv
import pandas
from pyspark import *
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *

sc = SparkContext("local")
sqlContext = SparkSession.builder.getOrCreate()

#########
print("loading the type data")
schema = StructType()\
	.add("subject",StringType(),True)\
	.add("relation",StringType(),True)\
	.add("object",StringType(),True)

instance_types_en = sqlContext.read.format('csv')\
	.options(delimiter=' ')\
	.schema(schema)\
	.load('instance_types_en.ttl')
instance_types_en.registerTempTable('instance_types_en')

print("filtering the relation data according to the relation type")
sqlContext.sql(u"""
	SELECT *
	FROM instance_types_en
	WHERE object LIKE "%dbpedia%org%ontology%"
	""").write.mode("Overwrite").json("instance_types_en")
instance_types_en = sqlContext.read.json("instance_types_en")
instance_types_en.registerTempTable("instance_types_en")

print("filter the relation data according to the picked entities")
sqlContext.sql(u"""
	SELECT t.* 
	FROM instance_types_en as t
	JOIN entity_count2 AS e
	ON e.entity = t.subject
	""").write.mode("Overwrite").json("instance_types_en1")
sqlContext.read.json("instance_types_en1").registerTempTable("instance_types_en1")

print("removed the multiple types of the same entity")
sqlContext.sql(u"""
	SELECT subject, 
	collect_set(relation)[0] as relation,
	collect_set(object)[0] as object
	from instance_types_en1
	group by subject
	""").write.mode("Overwrite").json("instance_types_en2")

sqlContext.read.json("instance_types_en2").registerTempTable("instance_types_en2")

'''
save to the ttl file
'''
print("saving the relation data to the ttl file")
sqlContext.sql(u"""
	SELECT CONCAT(subject, ' ', relation, ' ', object, ' . ')
	FROM instance_types_en2
	""").toPandas().to_csv(
	"instance_types_en_small.ttl",
	header = False,
	index = False,
	quoting = csv.QUOTE_NONE,
	quotechar="",  
	escapechar="\\",
	sep="\t")

#############jessica_dbpedia_type_filtering.py#############
