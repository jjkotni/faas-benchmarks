wsk -i action update native-app-audit-trail native-app-audit-trail.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000
wsk -i action update mpk-app-audit-trail    mpk-app-audit-trail.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000
wsk -i action update batch-app-audit-trail batch-app-audit-trail.zip  --docker openwhisk/python3aiaction --memory 512 --timeout 300000
wsk -i action update nativebatch-app-audit-trail nativebatch-app-audit-trail.zip --docker openwhisk/python3aiaction --memory 512 --timeout 300000