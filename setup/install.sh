#! /bin/bash

echo "Please input MySQL Server Address [default \"localhost\"]:"
read inputdata
if [ $inputdata ]
then
    mysqlAddr=$inputdata
else
    mysqlAddr="localhost"
fi

echo "Please input MySQL Server Port [default \"3306\"]:"
read inputdata
if [ $inputdata ]
then
    mysqlPort=$inputdata
else
    mysqlPort=3306
fi

echo "Please input MySQL User Name [default \"root\"]:"
read inputdata
if [ $inputdata ]
then
    mysqlUser=$inputdata
else
    mysqlUser="root"
fi

echo "Please input MySQL User" $mysqlUser "'s Password:"
read inputdata
mysqlPassword=$inputdata

echo "Please input MyAvatar Database Name [default \"avatar_test\"]:"
read inputdata
if [ $inputdata ]
then
    avatarDbName=$inputdata
else
    avatarDbName="avatar_test"
fi

echo $mysqlAddr $mysqlUser $mysqlPassword $avatarDbName

echo "Please input Apache Document Root [default \"/var/www\"]:"
read inputdata
if [ $inputdata ]
then
    documentRoot=$inputdata
else
    documentRoot="/var/www"
fi

# modify mysql info in account_info.py
filePath=account_info.py
sed -i "s/^_mysqlAddr = '\\w*'/_mysqlAddr = '${mysqlAddr}'/g" $filePath
sed -i "s/^_mysqlUser = '\\w*'/_mysqlUser = '${mysqlUser}'/g" $filePath
sed -i "s/^_rootPassword = '\\w*'/_rootPassword = '${mysqlPassword}'/g" $filePath
sed -i "s/^_avatardb = '\\w*'/_avatardb = '${avatarDbName}'/g" $filePath

sed -i "s/^DROP DATABASE \\w*;/DROP DATABASE ${avatarDbName};/g" avatar.sql
sed -i "s/^CREATE DATABASE \\w*;/CREATE DATABASE ${avatarDbName};/g" avatar.sql
sed -i "s/^USE \\w*;/USE ${avatarDbName};/g" avatar.sql

mysql -h $mysqlAddr -P $mysqlPort -u $mysqlUser -p$mysqlPassword < avatar.sql

# create DOCUMENT_ROOT/avatar
avatarPath=$documentRoot:/avatar
mkdir $avatarPath
chmod 777 $avatarPath
