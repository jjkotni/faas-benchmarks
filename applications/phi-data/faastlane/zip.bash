cp threads-main.py __main__.py
rm native-app-phi-data.zip
zip -r native-app-phi-data.zip __main__.py identifyphi.py deidentify.py anonymize.py virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/botocore virtualenv/lib/python3.5/site-packages/boto3 virtualenv/lib/python3.5/site-packages/jmespath virtualenv/lib/python3.5/site-packages/s3transfer

cp mpk-main.py __main__.py
rm mpk-app-phi-data.zip
zip -r mpk-app-phi-data.zip __main__.py identifyphi.py deidentify.py anonymize.py virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/botocore virtualenv/lib/python3.5/site-packages/boto3 virtualenv/lib/python3.5/site-packages/jmespath virtualenv/lib/python3.5/site-packages/s3transfer virtualenv/lib/python3.5/site-packages/mpkmemalloc.cpython-35m-x86_64-linux-gnu.so

cp batching-main.py __main__.py
rm batch-app-phi-data.zip
zip -r batch-app-phi-data.zip __main__.py identifyphi.py deidentify.py anonymize.py virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/botocore virtualenv/lib/python3.5/site-packages/boto3 virtualenv/lib/python3.5/site-packages/jmespath virtualenv/lib/python3.5/site-packages/s3transfer virtualenv/lib/python3.5/site-packages/mpkmemalloc.cpython-35m-x86_64-linux-gnu.so

cp native-batching-main.py __main__.py
rm nativebatch-app-phi-data.zip
zip -r nativebatch-app-phi-data.zip __main__.py identifyphi.py deidentify.py anonymize.py virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/botocore virtualenv/lib/python3.5/site-packages/boto3 virtualenv/lib/python3.5/site-packages/jmespath virtualenv/lib/python3.5/site-packages/s3transfer
