export WSK_CONFIG_FILE=/home/kjj/openwhisk-mod/.wskprops

BENCHMARKS=()

for ENTRY in *
do
    if [[ "$ENTRY" == *micro* ]]; then
        BENCHMARKS=( "${BENCHMARKS[@]}" "$ENTRY" )
    fi
done

wsk -i action list > tmp_actions
FILE_NAME=tmp_actions

for BENCHMARK in "${BENCHMARKS[@]}"
do
    ACTION_NAME=native-batch-${BENCHMARK%".py"}

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
