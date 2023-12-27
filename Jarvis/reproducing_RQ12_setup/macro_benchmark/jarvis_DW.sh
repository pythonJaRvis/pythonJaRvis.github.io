PjDir=$(pwd)/dataset/macro_benchmark/pj
# OutputDir=$(pwd)/reproducing_rq_result/macro_result
OutputDir=$(pwd)/output/macro_benchmark

Base=$(pwd)/tool
if [ ! -d "$OutputDir" ]; then

	mkdir -p $OutputDir
    mkdir -p $OutputDir/{bpytop,sshtunnel,rich-cli,furl,sqlparse,TextRank4ZH}/{pycg,jarvis}
fi


    echo 'bpytop analyze'
    pip3 install bpytop >/dev/null 2>&1
    # echo $PjDir/pj/bpytop/bpytop.py
    # echo $MacroDir/pj/bpytop
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/bpytop/bpytop.py --decy --package $PjDir/bpytop -o $OutputDir/bpytop/jarvis/jarvis_DW.json
    echo 'bpytop Done'

    echo 'sshtunnel analyze'
    pip3 install sshtunnel >/dev/null 2>&1
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/sshtunnel/sshtunnel.py --decy --package $PjDir/sshtunnel -o $OutputDir/sshtunnel/jarvis/jarvis_DW.json
    echo 'bpytop Done'

    echo 'furl analyze'
    pip3 install furl >/dev/null 2>&1
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/furl/furl/{omdict1D,__init__,__version__,common,compat,furl}.py --decy --package $PjDir/sshtunnel -o $OutputDir/sshtunnel/jarvis/jarvis_DW.json
    echo 'furl Done'


    echo 'rich-cli analyze'
    pip3 install rich-cli >/dev/null 2>&1
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/rich-cli/src/rich_cli/{__main__,__init__,markdown,pager,win_vt}.py --decy --package $PjDir/rich-cli/src -o $OutputDir/rich-cli/jarvis/jarvis_DW.json
    echo 'rich-cli Done'


    echo 'TextRank4ZH analyze'
    pip3 install textrank4zh >/dev/null 2>&1
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/TextRank4ZH/textrank4zh/{util,TextRank4Sentence,TextRank4Keyword,Segmentation}.py --decy --package $PjDir/TextRank4ZH -o $OutputDir/TextRank4ZH/jarvis/jarvis_DW.json
    echo 'rich-cli Done'

    echo 'sqlparse analyze'
    pip3 install sqlprase >/dev/null 2>&1
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/sqlparse/sqlparse/{utils,tokens,sql,keywords,lexer,formatter,exceptions,cli,__main__,__init__,engine/filter_stack,filters/right_margin,filters/tokens,filters/reindent,filters/output,filters/others,filters/__init__,filters/aligned_indent,engine/statement_splitter,engine/grouping,engine/__init__}.py --decy --package $PjDir/sqlparse -o $OutputDir/sqlparse/jarvis/jarvis_DW.json

    echo 'sqlparse Done'


