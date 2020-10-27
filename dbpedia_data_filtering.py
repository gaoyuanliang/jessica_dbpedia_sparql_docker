#############dbpedia_data_filtering.py#############
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

'''
load the data
'''

schema = StructType()\
	.add("subject",StringType(),True)\
	.add("relation",StringType(),True)\
	.add("object",StringType(),True)

mappingbased_objects_en = sqlContext.read.format('csv')\
	.options(delimiter=' ')\
	.schema(schema)\
	.load('mappingbased_objects_en.ttl')
mappingbased_objects_en.registerTempTable('mappingbased_objects_en')

'''
filter according to the relation
'''
sqlContext.sql(u"""
	SELECT *
	FROM mappingbased_objects_en
	WHERE relation LIKE "%dbpedia%org%ontology%"
	""").write.mode("Overwrite").json("mappingbased_objects_en1")

'''
count the subject and object of each entity
'''
mappingbased_objects_en1 = sqlContext.read.json("mappingbased_objects_en1")
mappingbased_objects_en1.registerTempTable('mappingbased_objects_en1')
#18111905

sqlContext.sql(u"""
	SELECT subject AS entity, COUNT(DISTINCT object) AS object_count
	FROM mappingbased_objects_en1
	GROUP BY subject
	""").write.mode('Overwrite').json('entity_object_count')

sqlContext.sql(u"""
	SELECT object AS entity, COUNT(DISTINCT subject) AS subject_count
	FROM mappingbased_objects_en1
	GROUP BY object
	""").write.mode('Overwrite').json('entity_subject_count')

sqlContext.read.json("entity_*_count").registerTempTable("entity_count")
sqlContext.sql(u"""
	SELECT entity, 
	CASE 
		WHEN object_count IS NULL THEN 0
		ELSE object_count
	END AS object_count,
	CASE 
		WHEN subject_count IS NULL THEN 0
		ELSE subject_count
	END AS subject_count
	FROM (
	SELECT entity, 
	COLLECT_SET(object_count)[0] AS object_count,
	COLLECT_SET(subject_count)[0] AS subject_count
	FROM entity_count
	GROUP BY entity
	) AS temp
	""").write.mode('Overwrite').json('entity_count1')

sqlContext.read.json("entity_count1").registerTempTable("entity_count1")

'''
sqlContext.sql(u"""
	SELECT * FROM entity_count1
	WHERE entity LIKE "%Mohammed_bin_Rashid_Al_Maktoum%"
	""").show(100, False)

+------------------------------------------------------------------------+------------+-------------+
|entity                                                                  |object_count|subject_count|
+------------------------------------------------------------------------+------------+-------------+
|<http://dbpedia.org/resource/Mohammed_bin_Rashid_Al_Maktoum>            |11          |69           |
|<http://dbpedia.org/resource/Manal_bint_Mohammed_bin_Rashid_Al_Maktoum> |4           |1            |
|<http://dbpedia.org/resource/Hamdan_bin_Mohammed_bin_Rashid_Al_Maktoum> |0           |1            |
|<http://dbpedia.org/resource/Maitha_bint_Mohammed_bin_Rashid_Al_Maktoum>|1           |0            |
|<http://dbpedia.org/resource/Maktoum_bin_Mohammed_bin_Rashid_Al_Maktoum>|0           |2            |
|<http://dbpedia.org/resource/Sheikh_Mohammed_bin_Rashid_Al_Maktoum>     |0           |2            |
|<http://dbpedia.org/resource/Majid_bin_Mohammed_bin_Rashid_Al_Maktoum>  |1           |0            |
+------------------------------------------------------------------------+------------+-------------+
'''


'''
sort the entities according to the sum of the subject and object count
pick the top 500000 entities
'''
sqlContext.sql(u"""
	SELECT *
	FROM entity_count1
	ORDER BY object_count+subject_count DESC
	LIMIT 500000
	""").write.mode('Overwrite').json('entity_count2')
#1797868

sqlContext.read.json("entity_count2").registerTempTable("entity_count2")

'''
sqlContext.sql(u"""
	SELECT * FROM entity_count2
	WHERE entity  LIKE "%Abu_Dhabi%"
	ORDER BY object_count+subject_count ASC
	""").show(100, False)
'''

'''
only keep the relations between the picked entities
'''
sqlContext.sql(u"""
	SELECT r.*
	FROM mappingbased_objects_en1 AS r
	JOIN  entity_count2 AS s ON s.entity = r.subject
	JOIN  entity_count2 AS o ON o.entity = r.object
	""").write.mode('Overwrite').json('mappingbased_objects_en_small')

sqlContext.read.json("mappingbased_objects_en_small").registerTempTable("mappingbased_objects_en_small")
sqlContext.sql(u"""
	SELECT COUNT(*) FROM mappingbased_objects_en_small
	""").show()
#228844

'''
save to a ttl file
'''
sqlContext.sql(u"""
	SELECT CONCAT(subject, ' ', relation, ' ', object, ' . ')
	FROM mappingbased_objects_en_small
	""").toPandas().to_csv(
	"mappingbased_objects_en_small.ttl",
	header = False,
	index = False,
	quoting = csv.QUOTE_NONE,
	quotechar="",  
	escapechar="\\",
	sep="\t")

#############dbpedia_data_filtering.py#############
