#Resize zip
cp resize.py __main__.py
rm resize.zip
zip -r resize.zip __main__.py data/image.jpg virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/botocore virtualenv/lib/python3.5/site-packages/boto3 virtualenv/lib/python3.5/site-packages/jmespath virtualenv/lib/python3.5/site-packages/s3transfer

#Predict zip
cp predict.py __main__.py
rm predict.zip
zip -r predict.zip __main__.py data/mobilenet_v2_1.0_224_frozen.pb virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/botocore virtualenv/lib/python3.5/site-packages/boto3 virtualenv/lib/python3.5/site-packages/jmespath virtualenv/lib/python3.5/site-packages/s3transfer
