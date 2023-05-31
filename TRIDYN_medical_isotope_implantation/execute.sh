INPUTDIR="/mnt/c/Users/r0750853/Linux/TRIDYN/"
FileList=("TbNN_5_060.in","TbNN_6_060.in")

for FILE in ${FileList[@]}; do
	echo filename is $FILE
	./tridyn2021_linux < $INPUTDIR$FILE

	NAME=$(head -c 10 $INPUTDIR$FILE)
 	ARDN=$"${NAME}_ardn.dat"
	DEPTH_NAMES=$(ls -d ${NAME}_pr*)
	DIR_ARDN=$"Simulated_data/Areal_density"
	DIR_DEPTH=$"Simulated_data/Depth_profile/${NAME}"
	DIR_REST=$"Simulated_data/Other"

	if [ ! -d $DIR_DEPTH ]; then
		mkdir $DIR_DEPTH
	fi


	mv -f $ARDN $DIR_ARDN

	for FILENAME in $DEPTH_NAMES; do
		mv -f $FILENAME $DIR_DEPTH
	done

	REST_NAMES=$(ls -d ${NAME}_*)
	for FILENAME in $REST_NAMES; do
		mv -f $FILENAME $DIR_REST
	done
done
