rm portfoliodata.zip
zip -r portfoliodata.zip __main__.py virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/botocore virtualenv/lib/python3.5/site-packages/boto3 virtualenv/lib/python3.5/site-packages/jmespath virtualenv/lib/python3.5/site-packages/certifi virtualenv/lib/python3.5/site-packages/chardet virtualenv/lib/python3.5/site-packages/s3transfer virtualenv/lib/python3.5/site-packages/multitasking 
# wsk -i action update portfoliodata.zip native-batch-app-audit-trail.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000
