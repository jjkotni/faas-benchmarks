wsk -i action update app-phi-data-anonymize anonymize.py --docker openwhisk/python3aiaction --timeout 1800000
wsk -i action update app-phi-data-deidentify deidentify.py --docker openwhisk/python3aiaction --timeout 1800000
wsk -i action update app-phi-data-identifyphi identifyphi.zip --docker openwhisk/python3aiaction --timeout 1800000
pycompose app.py > app.json
pydeploy baseline-app-phi-data app.json -i -w
