cp identifyphi.py __main__.py
rm app-phi-data-identifyphi.zip
zip -r app-phi-data-identifyphi.zip __main__.py virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/botocore virtualenv/lib/python3.5/site-packages/boto3 virtualenv/lib/python3.5/site-packages/jmespath virtualenv/lib/python3.5/site-packages/s3transfer
