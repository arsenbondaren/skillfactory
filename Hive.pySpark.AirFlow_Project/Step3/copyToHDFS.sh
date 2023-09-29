#!/bin/bash

fileName=$1
HDFSDir=$2
nameInDir=$3

if [ -z $3 ]
then
    echo Deleting $HDFSDir directory ...
    hdfs dfs -rm -r -skipTrash $HDFSDir >hdfs_stdout.txt 2>hdfs_stderr.txt
else
    echo Start copying $fileName to $HDFSDir/$nameInDir ...
    hdfs dfs -mkdir -p $HDFSDir >hdfs_stdout.txt 2>hdfs_stderr.txt
    hdfs dfs -put -f $fileName $HDFSDir/$nameInDir >hdfs_stdout.txt 2>hdfs_stderr.txt
fi

if [ $? -eq 0 ]
then
    echo Done, code $? 
else
    echo Some problem was detected, check hdfs_stderr.txt error code $?
fi
	


