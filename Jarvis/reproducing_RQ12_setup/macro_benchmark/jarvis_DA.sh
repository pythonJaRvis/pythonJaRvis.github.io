PjDir=$(pwd)/dataset/macro_benchmark/pj
OutputDir=$(pwd)/output/macro_benchmark

Base=$(pwd)/tool
if [ ! -d "$OutputDir" ]; then

	mkdir -p $OutputDir
    mkdir -p $OutputDir/{bpytop,sshtunnel,rich-cli,furl,sqlparse,TextRank4ZH}/{pycg,jarvis}
fi



    echo 'bpytop analyze'
    echo $PjDir/pj/bpytop/bpytop.py
    echo $MacroDir/pj/bpytop
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/bpytop/bpytop.py  --package $PjDir/bpytop --entry_point bpytop bpytop.main bpytop.Menu.help bpytop.Menu.main -o $OutputDir/bpytop/jarvis/jarvis_DA.json
    echo 'bpytop Done'

    echo 'sshtunnel analyze'
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/sshtunnel/sshtunnel.py  --package $PjDir/sshtunnel --entry_point sshtunnel -o $OutputDir/sshtunnel/jarvis/jarvis_DA.json
    echo 'bpytop Done'

    echo 'furl analyze'
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/furl/furl/{omdict1D,__init__,__version__,common,compat,furl}.py  --package $PjDir/sshtunnel --entry_point furl furl.furl.Path furl.furl.PathCompositionInterface furl.furl.Query furl.furl.QueryCompositionInterface furl.furl.FragmentCompositionInterface furl.furl.furl furl.furl.Path.normalize furl.furl.URLPathCompositionInterface._force_absolute furl.furl.furl.__truediv__ furl.furl.furl.asdict furl.furl.furl.join furl.omdict1D.omdict1D.__setitem__  -o $OutputDir/sshtunnel/jarvis/jarvis_DA.json
    echo 'furl Done'


    echo 'rich-cli analyze'
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/rich-cli/src/rich_cli/{__main__,__init__,markdown,pager,win_vt}.py  --package $PjDir/rich-cli/src --entry_point rich_cli.__main__ rich_cli.markdown rich_cli.pager rich_cli.win_vt -o $OutputDir/rich-cli/jarvis/jarvis_DA.json
    echo 'rich-cli Done'


    echo 'TextRank4ZH analyze'
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/TextRank4ZH/textrank4zh/{util,TextRank4Sentence,TextRank4Keyword,Segmentation}.py  --package $PjDir/TextRank4ZH   --entry_point textrank4zh  textrank4zh.TextRank4Keyword.TextRank4Keyword.__init__ textrank4zh.TextRank4Keyword.TextRank4Keyword.analyze textrank4zh.TextRank4Sentence.TextRank4Sentence.__init__ textrank4zh.TextRank4Sentence.TextRank4Sentence.analyze  -o $OutputDir/TextRank4ZH/jarvis/jarvis_DA.json
    echo $OutputDir/TextRank4ZH/jarvis/jarvis_DA.json
    echo 'rich-cli Done'

    echo 'sqlparse analyze'
    python3 $Base/Jarvis/jarvis_cli.py $PjDir/sqlparse/sqlparse/{utils,tokens,sql,keywords,lexer,formatter,exceptions,cli,__main__,__init__,engine/filter_stack,filters/right_margin,filters/tokens,filters/reindent,filters/output,filters/others,filters/__init__,filters/aligned_indent,engine/statement_splitter,engine/grouping,engine/__init__}.py  --package $PjDir/sqlparse --entry_point sqlparse sqlparse.cli sqlparse.cli.main sqlparse.engine.filter_stack sqlparse.engine.grouping sqlparse.engine.statement_splitter sqlparse.filters.aligned_indent sqlparse.filters.others sqlparse.filters.output sqlparse.filters.reindent sqlparse.filters.right_margin sqlparse.formatter sqlparse.keywords sqlparse.lexer sqlparse.parse sqlparse.split sqlparse.sql sqlparse.tokens sqlparse.utils sqlparse.exceptions sqlparse.filters sqlparse.lexer.Lexer sqlparse.sql.Comparison  -o $OutputDir/sqlparse/jarvis/jarvis_DA.json

    echo 'sqlparse Done'









