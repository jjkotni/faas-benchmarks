rm native-batch-app-prediction-pipeline.zip
zip -r native-batch-app-prediction-pipeline.zip __main__.py resize.py predict.py render.py virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/botocore virtualenv/lib/python3.5/site-packages/boto3 virtualenv/lib/python3.5/site-packages/jmespath virtualenv/lib/python3.5/site-packages/s3transfer 
wsk -i action update native-batch-app-prediction-pipeline native-batch-app-prediction-pipeline.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000
