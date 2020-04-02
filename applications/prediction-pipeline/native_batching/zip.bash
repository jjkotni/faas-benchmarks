rm native-batch-app-prediction-pipeline.zip
zip -r native-batch-app-prediction-pipeline.zip __main__.py resize.py predict.py render.py data/
wsk -i action update native-batch-app-prediction-pipeline native-batch-app-prediction-pipeline.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000
