rm mpk-app-prediction-pipeline.zip
zip -r mpk-app-prediction-pipeline.zip __main__.py resize.py predict.py render.py data/ virtualenv/bin/activate_this.py virtualenv/lib/python3.5/site-packages/mpkmemalloc.cpython-35m-x86_64-linux-gnu.so
wsk -i action update mpk-app-prediction-pipeline mpk-app-prediction-pipeline.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000
