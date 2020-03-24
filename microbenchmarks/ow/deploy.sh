BENCHMARKS=()

for ENTRY in *
do
    if [[ "$ENTRY" == *.py ]]; then
        BENCHMARKS=( "${BENCHMARKS[@]}" "$ENTRY" )
    fi
done

wsk -i action list > tmp_actions
FILE_NAME=tmp_actions

for BENCHMARK in "${BENCHMARKS[@]}"
do
    ACTION_NAME=${BENCHMARK%".py"}

	if grep -q $ACTION_NAME "$FILE_NAME"; then
	    echo "$ACTION_NAME action already defined, updating it..."
        wsk -i action update $ACTION_NAME $BENCHMARK --web true
	else
	    echo "Creating action $ACTION_NAME..."
        wsk -i action create $ACTION_NAME $BENCHMARK --web true
	fi

    echo "Testing action $ACTION_NAME"
    wsk -i action invoke $ACTION_NAME --result

done

rm tmp_actions

#Create sequences
# if grep -q 'baseline-micro-sequence-2fns' "$FILE_NAME"; then
#     echo "$ACTION_NAME action already defined, updating it..."
#     wsk -i action create baseline-micro-sequence-2fns --sequence input,square
# else
#     echo "Creating action $ACTION_NAME..."
#     wsk -i action update baseline-micro-sequence-2fns --sequence input,square
# fi

# if grep -q 'baseline-micro-sequence-2fns' "$FILE_NAME"; then
#     echo "$ACTION_NAME action already defined, updating it..."
#     wsk -i action create baseline-micro-sequence-5fns --sequence input,increment,square,half,reminder
# else
#     echo "Creating action $ACTION_NAME..."
#     wsk -i action update baseline-micro-sequence-5fns --sequence input,increment,square,half,reminder
# fi
