wsk -i action update marginbalance marginBalance.zip --kind python:ai --memory 128 --timeout 1800000
wsk -i action update marketdata marketdata.zip --kind python:ai  --memory 128 --timeout 1800000
wsk -i action update lastpx lastpx.zip --kind python:ai  --memory 128 --timeout 1800000
wsk -i action update side side.zip --kind python:ai  --memory 128 --timeout 1800000
wsk -i action update volume volume.zip --kind python:ai  --memory 128 --timeout 1800000
wsk -i action update trddate trddate.zip --kind python:ai  --memory 128 --timeout 1800000
wsk -i action update trdsubtype trdsubtype.zip --kind python:ai  --memory 128 --timeout 1800000

#Deploy the composed action
compose baseline-app-audit-trail.js > baseline-app-audit-trail.json
deploy baseline-app-audit-trail baseline-app-audit-trail.json -t 1800000 -i -w
