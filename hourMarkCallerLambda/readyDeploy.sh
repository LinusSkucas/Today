#!/usr/bin/env bash

echo '🥨 Preparing...'
rm -f function.zip
echo '🍳 Making Virtual Environment...'
virtualenv --python=python3.7 deployment-env
source deployment-env/bin/activate
echo '🎓 Installing Requirements...'
pip3 install -r requirements.txt
deactivate
echo '🦉 Zipping 3rd Party Packages up...'
cd deployment-env/lib/python3.7/site-packages
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
echo '🧨 Zipping the Function up...'
zip -g function.zip hourMarkLambdaFunction.py
echo '🚀 Uploading to AWS!'
aws lambda update-function-code --function-name hourMarkCaller --zip-file fileb://function.zip
echo '🛀🏼 Cleaning up...'
rm -rf deployment-env
echo '✅ Success!'
