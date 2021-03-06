BENCHMARKS=()

for ENTRY in *
do
    if [[ "$ENTRY" == *.py ]]; then
        BENCHMARKS=( "${BENCHMARKS[@]}" "$ENTRY" )
    fi
done

FILE_NAME=tmp_actions
wsk -i action list > $FILE_NAME

for BENCHMARK in "${BENCHMARKS[@]}"
do
    ACTION_NAME=${BENCHMARK%".py"}
    wsk -i action update $ACTION_NAME $BENCHMARK --web true
    # echo "Testing action $ACTION_NAME"
    # wsk -i action invoke $ACTION_NAME --param-file number.json --result
done

#Create sequences
wsk -i action update baseline-micro-sequence-2fns --sequence input,square --timeout 1800000
# wsk -i action invoke baseline-micro-sequence-2fns --result

wsk -i action update baseline-micro-sequence-5fns --sequence input,increment,square,half,reminder --timeout 1800000
# wsk -i action invoke baseline-micro-sequence-5fns --result

deploy baseline-micro-parallel-2fns baseline-micro-parallel-2fns.json -i -w
# wsk -i action invoke baseline-micro-parallel-2fns --param-file redis.json --result

deploy baseline-micro-parallel-5fns baseline-micro-parallel-5fns.json -i -w
# wsk -i action invoke baseline-micro-parallel-5fns --param-file redis.json --result

pydeploy baseline-micro-choice-2fns baseline-micro-choice-2fns.json -i -w
# wsk -i action invoke baseline-micro-choice-2fns --param-file redis.json --result

rm $FILE_NAME
