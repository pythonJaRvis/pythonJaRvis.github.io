#!/bin/bash
Path=$(pwd)/dataset/micro_benchmark
OutputDir=$(pwd)/output/micro_benchmark
Base=$(pwd)/tool

start_pycg(){
	if [ ! -d "$OutputDir" ]; then
		mkdir -p "$OutputDir"
	fi
    # pip3 install pycg
	for element in `ls $1`
	do
		file=$1"/"$element
		if [ -d $file ]
		then
			start_pycg $file
		elif [ "${file##*.}"x = "py"x ]
		then
			if [ ${file##*/}x = 'main.py'x ]
			then
				parent_directory="$(dirname "$file")"
				parent_filename="$(basename "$parent_directory")"

				p_parent_directory="$(dirname "$parent_directory")"
				p_parent_filename="$(basename "$p_parent_directory")"
				output_dir=${OutputDir}/$p_parent_filename/$parent_filename
				if [ ! -d "$output_dir" ]; then
    				mkdir -p "$output_dir"
				fi
				output_pycg="$output_dir/pycg.json"
				output_jarvis="$output_dir/jarvis.json"
#				echo $output_pycg
				python3 $Base/pycg/__main__.py  --package ${file%/*} --noclass -o $output_pycg
				python3 $Base/Jarvis/jarvis_cli.py $file --precision --package ${file%/*} -o $output_jarvis
 
			fi
		fi
	done
}
start_pycg $Path

