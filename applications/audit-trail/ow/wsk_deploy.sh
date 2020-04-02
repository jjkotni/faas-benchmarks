wsk -i action update marginbalance marginbalance.py --docker openwhisk/python3aiaction --memory 512
wsk -i action update portfoliodata portfoliodata.zip --docker openwhisk/python3aiaction --memory 512
wsk -i action update marketdata marketdata.zip --docker openwhisk/python3aiaction --memory 512

#Deploy the composed action
compose baseline-app-audit-trail.js > baseline-app-audit-trail.json
deploy baseline-app-audit-trail baseline-app-audit-trail.json -i -w
