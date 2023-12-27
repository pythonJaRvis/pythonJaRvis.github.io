PjDir=$(pwd)/dataset/macro_benchmark/pj
# OutputDir=$(pwd)/reproducing_rq_result/macro_result/pycg
OutputDir=$(pwd)/output/macro_benchmark

Base=$(pwd)/tool
if [ ! -d "$OutputDir" ]; then

	mkdir -p $OutputDir
    mkdir -p $OutputDir/{bpytop,sshtunnel,rich-cli,furl,sqlparse,TextRank4ZH}/{pycg,jarvis}
fi

pip3 install pycg >/dev/null 2>&1

echo "Iterate once"
python3 $(pwd)/tool/pycg/__main__.py  $PjDir/bpytop/bpytop.py --max-iter 1 --package $PjDir/bpytop --nodecy -o $OutputDir/bpytop/pycg/pycg_EA_1.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/sshtunnel/sshtunnel.py --max-iter 1 --package $PjDir/sshtunnel --nodecy -o $OutputDir/sshtunnel/pycg/pycg_EA_1.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/furl/furl/{omdict1D,__init__,__version__,common,compat,furl}.py --max-iter 1 --package $PjDir/furl --nodecy -o $OutputDir/furl/pycg/pycg_EA_1.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/rich-cli/src/rich_cli/{__main__,__init__,markdown,pager,win_vt}.py  --max-iter 1  --package $PjDir/rich-cli/src --nodecy -o $OutputDir/rich-cli/pycg/pycg_EA_1.json

python3 $(pwd)/tool/pycg/__main__.py $Base/Jarvis/jarvis_cli.py $PjDir/TextRank4ZH/textrank4zh/{util,TextRank4Sentence,TextRank4Keyword,Segmentation}.py --max-iter 1 --package $PjDir/TextRank4ZH --nodecy -o $OutputDir/TextRank4ZH/pycg/pycg_EA_1.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/sqlparse/sqlparse/{utils,tokens,sql,keywords,lexer,formatter,exceptions,cli,__main__,__init__,engine/filter_stack,filters/right_margin,filters/tokens,filters/reindent,filters/output,filters/others,filters/__init__,filters/aligned_indent,engine/statement_splitter,engine/grouping,engine/__init__}.py  --max-iter 1 --package $PjDir/sqlparse --nodecy -o $OutputDir/sqlparse/pycg/pycg_EA_1.json

echo "Iterate twice"
python3 $(pwd)/tool/pycg/__main__.py  $PjDir/bpytop/bpytop.py --max-iter 2 --package $PjDir/bpytop --nodecy -o $OutputDir/bpytop/pycg/pycg_EA_2.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/sshtunnel/sshtunnel.py --max-iter 2 --package $PjDir/sshtunnel --nodecy -o $OutputDir/sshtunnel/pycg/pycg_EA_2.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/furl/furl/{omdict1D,__init__,__version__,common,compat,furl}.py --max-iter 2 --package $PjDir/furl --nodecy -o $OutputDir/furl/pycg/pycg_EA_2.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/rich-cli/src/rich_cli/{__main__,__init__,markdown,pager,win_vt}.py  --max-iter 2  --package $PjDir/rich-cli/src --nodecy -o $OutputDir/rich-cli/pycg/pycg_EA_2.json

python3 $(pwd)/tool/pycg/__main__.py $Base/Jarvis/jarvis_cli.py $PjDir/TextRank4ZH/textrank4zh/{util,TextRank4Sentence,TextRank4Keyword,Segmentation}.py --max-iter 2 --package $PjDir/TextRank4ZH --nodecy -o $OutputDir/TextRank4ZH/pycg/pycg_EA_2.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/sqlparse/sqlparse/{utils,tokens,sql,keywords,lexer,formatter,exceptions,cli,__main__,__init__,engine/filter_stack,filters/right_margin,filters/tokens,filters/reindent,filters/output,filters/others,filters/__init__,filters/aligned_indent,engine/statement_splitter,engine/grouping,engine/__init__}.py  --max-iter 2 --package $PjDir/sqlparse --nodecy -o $OutputDir/sqlparse/pycg/pycg_EA_2.json


echo "Iterate to convergence"
python3 $(pwd)/tool/pycg/__main__.py  $PjDir/bpytop/bpytop.py  --package $PjDir/bpytop --nodecy -o $OutputDir/bpytop/pycg/pycg_EA_m.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/sshtunnel/sshtunnel.py  --package $PjDir/sshtunnel --nodecy -o $OutputDir/sshtunnel/pycg/pycg_EA_m.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/furl/furl/{omdict1D,__init__,__version__,common,compat,furl}.py  --package $PjDir/furl --nodecy -o $OutputDir/furl/pycg/pycg_EA_m.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/rich-cli/src/rich_cli/{__main__,__init__,markdown,pager,win_vt}.py  --package $PjDir/rich-cli/src --nodecy -o $OutputDir/rich-cli/pycg/pycg_EA_m.json

python3 $(pwd)/tool/pycg/__main__.py $Base/Jarvis/jarvis_cli.py $PjDir/TextRank4ZH/textrank4zh/{util,TextRank4Sentence,TextRank4Keyword,Segmentation}.py  --package $PjDir/TextRank4ZH --nodecy -o $OutputDir/TextRank4ZH/pycg/pycg_EA_m.json

python3 $(pwd)/tool/pycg/__main__.py  $PjDir/sqlparse/sqlparse/{utils,tokens,sql,keywords,lexer,formatter,exceptions,cli,__main__,__init__,engine/filter_stack,filters/right_margin,filters/tokens,filters/reindent,filters/output,filters/others,filters/__init__,filters/aligned_indent,engine/statement_splitter,engine/grouping,engine/__init__}.py  --package $PjDir/sqlparse --nodecy -o $OutputDir/sqlparse/pycg/pycg_EA_m.json


