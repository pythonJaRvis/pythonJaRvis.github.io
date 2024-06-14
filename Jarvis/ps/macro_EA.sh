# PjDir=$(pwd)/dataset/macro_benchmark/pj
PjDir=/Users/yixuanyan/yyx/github/jarvis/Jarvis/dataset/macro_benchmark/pj
# OutputDir=$(pwd)/reproducing_rq_result/macro_result/pycg
# OutputDir=$(pwd)/output/macro_benchmark
OutputDir=/Users/yixuanyan/yyx/github/jarvis/Jarvis/ps
# Base=$(pwd)/tool
if [ ! -d "$OutputDir" ]; then

	mkdir -p $OutputDir
    mkdir -p $OutputDir/{bpytop,sshtunnel,rich-cli,furl,sqlparse,TextRank4ZH}/{pycg,jarvis}
fi

# pip3 install code2flow >/dev/null 2>&1

/usr/bin/time -lp  code2flow  $PjDir/bpytop/bpytop.py --output $OutputDir/bpytop/EA.json > $OutputDir/bpytop/EA.txt 2>&1

/usr/bin/time -lp  code2flow  $PjDir/sshtunnel/sshtunnel.py --output $OutputDir/sshtunnel/EA.json > $OutputDir/sshtunnel/EA.txt 2>&1

/usr/bin/time -lp  code2flow  $PjDir/furl/furl/{omdict1D,__init__,__version__,common,compat,furl}.py --output $OutputDir/furl/EA.json > $OutputDir/furl/EA.txt 2>&1

/usr/bin/time -lp  code2flow  $PjDir/rich-cli/src/rich_cli/{__main__,__init__,markdown,pager,win_vt}.py  --output $OutputDir/rich-cli/EA.json > $OutputDir/rich-cli/EA.txt 2>&1

/usr/bin/time -lp  code2flow $Base/Jarvis/jarvis_cli.py $PjDir/TextRank4ZH/textrank4zh/{util,TextRank4Sentence,TextRank4Keyword,Segmentation}.py --output $OutputDir/TextRank4ZH/EA.json > $OutputDir/TextRank4ZH/EA.txt 2>&1

/usr/bin/time -lp  code2flow  $PjDir/sqlparse/sqlparse/{utils,tokens,sql,keywords,lexer,formatter,exceptions,cli,__main__,__init__,engine/filter_stack,filters/right_margin,filters/tokens,filters/reindent,filters/output,filters/others,filters/__init__,filters/aligned_indent,engine/statement_splitter,engine/grouping,engine/__init__}.py  --output $OutputDir/sqlparse/EA.json > $OutputDir/sqlparse/EA.txt 2>&1

