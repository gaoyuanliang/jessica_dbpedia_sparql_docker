############Dockerfile############
FROM python:3.7

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y git 
RUN apt-get install -y curl
RUN apt-get install -y bzip2
RUN apt-get install -y openjdk-11-jdk

RUN pip install rdflib==5.0.0
RUN pip install requests==2.24.0
RUN pip install pyspark==3.0.1
RUN pip install pandas==1.1.3

RUN wget http://downloads.dbpedia.org/2016-10/core-i18n/en/mappingbased_objects_en.ttl.bz2

RUN bzip2 -d mappingbased_objects_en.ttl.bz2

RUN echo "gsdg"
RUN wget https://raw.githubusercontent.com/gaoyuanliang/jessica_dbpedia_sparql_docker/main/jessica_dbpedia_data_filtering.py
RUN python jessica_dbpedia_data_filtering.py

RUN git clone https://github.com/gaoyuanliang/jessica_dbpedia_sparql_docker.git
RUN mv jessica_dbpedia_sparql_docker/* ./

CMD bash
############Dockerfile############
