wsk -i action update native-app-phi-data native-app-phi-data.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000
wsk -i action update mpk-app-phi-data    mpk-app-phi-data.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000
# wsk -i action update batch-app-phi-data batch-app-phi-data.zip  --docker openwhisk/python3aiaction --memory 512 --timeout 300000
# wsk -i action update nativebatch-app-phi-data nativebatch-app-phi-data.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000
