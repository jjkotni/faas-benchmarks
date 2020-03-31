wsk -i action update app-prediction-pipeline-resize resize.zip --docker openwhisk/python3aiaction --memory 512
wsk -i action update app-prediction-pipeline-predict predict.zip --docker openwhisk/python3aiaction --memory 512
wsk -i action update app-prediction-pipeline-render render.py --docker openwhisk/python3aiaction --memory 512
wsk -i action update baseline-app-prediction-pipeline --sequence app-prediction-pipeline-resize,app-prediction-pipeline-predict,app-prediction-pipeline-render
