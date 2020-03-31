#Threads only
wsk -i action update native-app-prediction-pipeline threads/native-app-prediction-pipeline.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000

#MPK
wsk -i action update mpk-app-prediction-pipeline mpk/mpk-app-prediction-pipeline.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000

#Batching
wsk -i action update batch-app-prediction-pipeline batching/batch-app-prediction-pipeline.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000

#Baseline
wsk -i action update app-prediction-pipeline-resize ow/resize.zip --docker openwhisk/python3aiaction --memory 512
wsk -i action update app-prediction-pipeline-predict ow/predict.zip --docker openwhisk/python3aiaction --memory 512
wsk -i action update app-prediction-pipeline-render ow/render.py --docker openwhisk/python3aiaction --memory 512
wsk -i action update baseline-app-prediction-pipeline --sequence app-prediction-pipeline-resize,app-prediction-pipeline-predict,app-prediction-pipeline-render --timeout 300000
