# PjDir=$(pwd)/dataset/macro_benchmark/pj
PjDir=/Users/yixuanyan/yyx/github/jarvis/Jarvis/ps
# OutputDir=$(pwd)/reproducing_rq_result/macro_result/pycg
# OutputDir=$(pwd)/output/macro_benchmark
OutputDir=/Users/yixuanyan/yyx/github/jarvis/Jarvis/ps
# Base=$(pwd)/tool
# if [ ! -d "$OutputDir" ]; then

# 	mkdir -p $OutputDir
#     mkdir -p $OutputDir/{bpytop,sshtunnel,rich-cli,furl,sqlparse,TextRank4ZH}/{pycg,jarvis}
# fi

/usr/bin/time -lp  code2flow $(cat $PjDir/bpytop/bpytop.txt) --output $OutputDir/bpytop/EW.json > $OutputDir/bpytop/EW.txt 2>&1

/usr/bin/time -lp  code2flow  $(cat $PjDir/sshtunnel/sshtunnel.txt) --output $OutputDir/sshtunnel/EW.json > $OutputDir/sshtunnel/EW.txt 2>&1

/usr/bin/time -lp  code2flow  $(cat $PjDir/furl/furl.txt) --output $OutputDir/furl/EW.json > $OutputDir/furl/EW.txt 2>&1

/usr/bin/time -lp  code2flow  $(cat $PjDir/rich-cli/rich-cli.txt)  --output $OutputDir/rich-cli/EW.json > $OutputDir/rich-cli/EW.txt 2>&1

/usr/bin/time -lp  code2flow  $(cat $PjDir/TextRank4ZH/TextRank4ZH.txt) --output $OutputDir/TextRank4ZH/EW.json > $OutputDir/bpytop/EW.txt 2>&1

/usr/bin/time -lp  code2flow  $(cat $PjDir/sqlparse/sqlparse.txt)  --output $OutputDir/sqlparse/EW.json > $OutputDir/sqlparse/EW.txt 2>&1

