rm native-app-prediction-pipeline.zip
zip -r native-app-prediction-pipeline.zip __main__.py resize.py predict.py render.py util.py data/
wsk -i action update native-app-prediction-pipeline native-app-prediction-pipeline.zip --kind python:ai --memory 2048 --timeout 300000
