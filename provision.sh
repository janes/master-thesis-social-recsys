#!/usr/bin/env bash
 
echo 'export LC_ALL="en_US.UTF-8"' >> /home/vagrant/.bashrc
 
echo '----------------------------------------------'
echo ' INSTALLING JAVA, GIT and MAVEN'
echo '----------------------------------------------'
apt-get update
apt-get -y --force-yes install \
openjdk-7-jdk \
git \
maven \
htop 

echo '----------------------------------------------'
echo ' INSTALLING MONGODB'
echo '----------------------------------------------'
sudo apt-get update
sudo apt-get install -y mongodb

echo '----------------------------------------------'
echo ' INSTALLING TOMCAT'
echo '----------------------------------------------'
sudo apt-get update
sudo apt-get install -y tomcat7

echo '----------------------------------------------'
echo ' INSTALLING JAVA                              '
echo '----------------------------------------------'
apt-get -y --force-yes install \
openjdk-7-jdk \
htop

echo '----------------------------------------------'
echo ' INSTALLING SPARK                             '
echo '----------------------------------------------'
mkdir /home/vagrant/packages
chown -R vagrant:vagrant /home/vagrant/packages
wget -P /home/vagrant/packages http://ftp.unicamp.br/pub/apache/spark/spark-1.4.1/spark-1.4.1-bin-hadoop2.6.tgz
tar -zxvf /home/vagrant/packages/spark-1.4.1-bin-hadoop2.6.tgz -C /home/vagrant/packages

echo 'export PATH="/home/vagrant/packages/spark-1.4.1-bin-hadoop2.6/bin:$PATH"' >> /home/vagrant/.bashrc
source ~/.bashrc

echo '----------------------------------------------'
echo ' INSTALLING PYTHON STUFF                          '
echo '----------------------------------------------'
apt-get -y --force-yes install \
python-pip \
python-numpy

pip install nltk
pip install pymongo

touch nltk_download.py
printf "import nltk\nnltk.download('punkt')\nnltk.download('stopwords')\nnltk.download('maxent_treebank_pos_tagger')" > nltk_download.py
python nltk_download.py
rm nltk_download.py


