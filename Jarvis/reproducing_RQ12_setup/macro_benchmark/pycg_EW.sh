PjDir=$(pwd)/dataset/macro_benchmark/pj
# OutputDir=$(pwd)/reproducing_rq_result/macro_result/pycg
OutputDir=$(pwd)/output/macro_benchmark

Base=$(pwd)/tool
if [ ! -d "$OutputDir" ]; then

	mkdir -p $OutputDir
    mkdir -p $OutputDir/{bpytop,sshtunnel,rich-cli,furl,sqlparse,TextRank4ZH}/{pycg,jarvis}
fi

if [ "$#" -eq 0 ]; then
    echo 'bpytop analyze'
    pip3 install bpytop >/dev/null 2>&1
    # echo $PjDir/pj/bpytop/bpytop.py
    # echo $MacroDir/pj/bpytop
    python3 $Base/pycg/__main__.py $PjDir/bpytop/bpytop.py  --package $PjDir/bpytop -o $OutputDir/bpytop/pycg/pycg_EW_m.json
    echo 'bpytop Done'

    echo 'sshtunnel analyze'
    pip3 install sshtunnel >/dev/null 2>&1
    python3 $Base/pycg/__main__.py $PjDir/sshtunnel/sshtunnel.py  --package $PjDir/sshtunnel -o $OutputDir/sshtunnel/pycg/pycg_EW_m.json
    echo 'bpytop Done'

    echo 'furl analyze'
    pip3 install furl >/dev/null 2>&1
    python3 $Base/pycg/__main__.py $PjDir/furl/furl/{omdict1D,__init__,__version__,common,compat,furl}.py  --package $PjDir/furls -o $OutputDir/furl/pycg/pycg_EW_m.json
    echo 'furl Done'


    echo 'rich-cli analyze'
    pip3 install rich-cli >/dev/null 2>&1
    python3 $Base/pycg/__main__.py $PjDir/rich-cli/src/rich_cli/{__main__,__init__,markdown,pager,win_vt}.py  --package $PjDir/rich-cli/src -o $OutputDir/rich-cli/pycg/pycg_EW_m.json
    echo 'rich-cli Done'


    echo 'TextRank4ZH analyze'
    pip3 install textrank4zh >/dev/null 2>&1
    python3 $Base/pycg/__main__.py $PjDir/TextRank4ZH/textrank4zh/{util,TextRank4Sentence,TextRank4Keyword,Segmentation}.py  --package $PjDir/TextRank4ZH -o $OutputDir/TextRank4ZH/pycg/pycg_EW_m.json
    echo $OutputDir/TextRank4ZH/pycg_ew_1.json
    echo 'rich-cli Done'

    echo 'sqlparse analyze'
    pip3 install sqlprase >/dev/null 2>&1
    python3 $Base/pycg/__main__.py $PjDir/sqlparse/sqlparse/{utils,tokens,sql,keywords,lexer,formatter,exceptions,cli,__main__,__init__,engine/filter_stack,filters/right_margin,filters/tokens,filters/reindent,filters/output,filters/others,filters/__init__,filters/aligned_indent,engine/statement_splitter,engine/grouping,engine/__init__}.py  --package $PjDir/sqlparse -o $OutputDir/sqlparse/pycg/pycg_EW_m.json

    echo 'sqlparse Done'

else
    arg="$1"
    if [[ $arg =~ ^[1-9][0-9]*$ ]]; then
        echo 'bpytop analyze'
        pip3 install bpytop >/dev/null 2>&1
        # echo $PjDir/pj/bpytop/bpytop.py
        # echo $MacroDir/pj/bpytop
        python3 $Base/pycg/__main__.py $PjDir/bpytop/bpytop.py --max-iter "$arg" --package $PjDir/bpytop -o $OutputDir/bpytop/pycg_ew_$arg.json
        echo 'bpytop Done'

        echo 'sshtunnel analyze'
        pip3 install sshtunnel >/dev/null 2>&1
        python3 $Base/pycg/__main__.py $PjDir/sshtunnel/sshtunnel.py  --max-iter "$arg"  --package $PjDir/sshtunnel -o $OutputDir/sshtunnel/pycg_ew_$arg.json
        echo 'bpytop Done'

        echo 'furl analyze'
        pip3 install furl >/dev/null 2>&1
        python3 $Base/pycg/__main__.py $PjDir/furl/furl/{omdict1D,__init__,__version__,common,compat,furl}.py   --max-iter "$arg"  --package $PjDir/furl -o $OutputDir/furl/pycg_ew_$arg.json
        echo 'furl Done'


        echo 'rich-cli analyze'
        pip3 install rich-cli >/dev/null 2>&1
        python3 $Base/pycg/__main__.py $PjDir/rich-cli/src/rich_cli/{__main__,__init__,markdown,pager,win_vt}.py   --max-iter "$arg"  --package $PjDir/rich-cli/src -o $OutputDir/rich-cli/pycg_ew_$arg.json
        echo 'rich-cli Done'


        echo 'TextRank4ZH analyze'
        pip3 install textrank4zh >/dev/null 2>&1
        python3 $Base/pycg/__main__.py $PjDir/TextRank4ZH/textrank4zh/{util,TextRank4Sentence,TextRank4Keyword,Segmentation}.py   --max-iter "$arg" --package $PjDir/TextRank4ZH -o $OutputDir/TextRank4ZH/pycg_ew_$arg.json
        echo 'rich-cli Done'

        echo 'sqlparse analyze'
        pip3 install sqlprase >/dev/null 2>&1
        python3 $Base/pycg/__main__.py $PjDir/sqlparse/sqlparse/{utils,tokens,sql,keywords,lexer,formatter,exceptions,cli,__main__,__init__,engine/filter_stack,filters/right_margin,filters/tokens,filters/reindent,filters/output,filters/others,filters/__init__,filters/aligned_indent,engine/statement_splitter,engine/grouping,engine/__init__}.py  --package $PjDir/sqlparse  --max-iter "$arg"  -o $OutputDir/sqlparse/pycg_ew_$arg.json
        echo 'sqlparse Done'
    else
        echo "Invalid argument. Please provide a numeric value (0-99)."
    fi
fi