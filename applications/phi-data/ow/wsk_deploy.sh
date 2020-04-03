wsk -i action update app-phi-data-anonymize --docker openwhisk/python3aiaction --timeout 1800000
wsk -i action update app-phi-data-deidentify --docker openwhisk/python3aiaction --timeout 1800000
wsk -i action update app-phi-data-identifyphi --docker openwhisk/python3aiaction --timeout 1800000

pydeploy baseline-app-phi-data app.json -i -w -t 1800000
