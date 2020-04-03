wsk -i action update marginbalance marginbalance.py --docker openwhisk/python3aiaction --memory 512 --timeout 1800000
wsk -i action update portfoliodata portfoliodata.zip --docker openwhisk/python3aiaction --memory 512 --timeout 1800000
wsk -i action update marketdata marketdata.zip --docker openwhisk/python3aiaction --memory 512 --timeout 1800000

#Deploy the composed action
compose baseline-app-audit-trail.js > baseline-app-audit-trail.json
deploy baseline-app-audit-trail baseline-app-audit-trail.json -i -w -A limits=limits.json
