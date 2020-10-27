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

RUN pip install gdown
RUN gdown https://drive.google.com/uc?id=1iKkzwZsmTBBbk8O351qQp-hb3dV3yOB7
RUN gdown https://drive.google.com/uc?id=1zaXTgJA7VpjSKXc8QjI3WLkbYf_vMZ8k

RUN echo "gsdg"

RUN git clone https://github.com/gaoyuanliang/jessica_dbpedia_sparql_docker.git
RUN mv jessica_dbpedia_sparql_docker/* ./

CMD bash
############Dockerfile############
