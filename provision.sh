#!/usr/bin/env bash
 
echo 'export LC_ALL="en_US.UTF-8"' >> /home/vagrant/.bashrc
 
echo '----------------------------------------------'
echo ' INSTALLING JAVA, GIT and MAVEN'
echo '----------------------------------------------'
sudo add-apt-repository ppa:webupd8team/java -y
sudo apt-get update
echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
sudo apt-get -y install oracle-java8-installer
sudo apt-get -y install oracle-java8-set-default

sudo apt-get -y install maven

echo '----------------------------------------------'
echo ' INSTALLING MONGODB'
echo '----------------------------------------------'
sudo apt-get update
sudo apt-get install -y mongodb

echo '----------------------------------------------'
echo ' INSTALLING TOMCAT'
echo '----------------------------------------------'
wget http://ftp.unicamp.br/pub/apache/tomcat/tomcat-7/v7.0.67/bin/apache-tomcat-7.0.67.tar.gz
tar -xvf apache-tomcat-7.0.67.tar.gz

echo '----------------------------------------------'
echo ' INSTALLING SPARK                             '
echo '----------------------------------------------'
wget  http://ftp.unicamp.br/pub/apache/spark/spark-1.4.1/spark-1.4.1-bin-hadoop2.6.tgz
tar -zxvf spark-1.4.1-bin-hadoop2.6.tgz 

#echo 'export PATH="/home/vagrant/packages/spark-1.4.1-bin-hadoop2.6/bin:$PATH"' >> /home/vagrant/.bashrc
#source ~/.bashrc

echo '----------------------------------------------'
echo ' INSTALLING PYTHON STUFF                          '
echo '----------------------------------------------'
sudo apt-get -y --force-yes install \
python-pip \
python-numpy

sudo pip install nltk
sudo pip install pymongo

# For scrapy...
sudo apt-get install -y libxml2-dev libxslt1-dev python-dev libffi-dev libssl-dev libyaml-0-2 libyaml-dev
sudo pip install scrapy

touch nltk_download.py
printf "import nltk\nnltk.download('punkt')\nnltk.download('stopwords')\nnltk.download('maxent_treebank_pos_tagger')" > nltk_download.py
python nltk_download.py
rm nltk_download.py


