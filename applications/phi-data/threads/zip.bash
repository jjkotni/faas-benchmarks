rm native-app-phi-data.zip

zip -r native-app-phi-data.zip __main__.py identifyphi.py deidentify.py anonymize.py analytics.py util.py virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/botocore virtualenv/lib/python3.5/site-packages/boto3 virtualenv/lib/python3.5/site-packages/jmespath virtualenv/lib/python3.5/site-packages/s3transfer
