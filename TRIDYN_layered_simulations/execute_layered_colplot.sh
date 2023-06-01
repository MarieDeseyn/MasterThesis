INPUTDIR="/mnt/c/Users/r0750853/Documents/layeredcolorplot_morers2_ownact/"
FileList=("TbGd_l00_0.in" "TbGd_l00_1.in" "TbGd_l00_2.in" "TbGd_l00_3.in" "TbGd_l01_0.in" "TbGd_l01_1.in" "TbGd_l01_2.in" "TbGd_l01_3.in" "TbGd_l02_0.in" "TbGd_l02_1.in" "TbGd_l02_2.in" "TbGd_l02_3.in" "TbGd_l03_0.in" "TbGd_l03_1.in" "TbGd_l03_2.in" "TbGd_l03_3.in" "TbGd_l04_0.in" "TbGd_l04_1.in" "TbGd_l04_2.in" "TbGd_l04_3.in" "TbGd_l05_0.in" "TbGd_l05_1.in" "TbGd_l05_2.in" "TbGd_l05_3.in" "TbGd_l06_0.in" "TbGd_l06_1.in" "TbGd_l06_2.in" "TbGd_l06_3.in" "TbGd_l07_0.in" "TbGd_l07_1.in" "TbGd_l07_2.in" "TbGd_l07_3.in" "TbGd_l08_0.in" "TbGd_l08_1.in" "TbGd_l08_2.in" "TbGd_l08_3.in" "TbGd_l09_0.in" "TbGd_l09_1.in" "TbGd_l09_2.in" "TbGd_l09_3.in" "TbGd_l10_0.in" "TbGd_l10_1.in" "TbGd_l10_2.in" "TbGd_l10_3.in" "TbGd_l11_0.in" "TbGd_l11_1.in" "TbGd_l11_2.in" "TbGd_l11_3.in" "TbGd_l12_0.in" "TbGd_l12_1.in" "TbGd_l12_2.in" "TbGd_l12_3.in" "TbGd_l13_0.in" "TbGd_l13_1.in" "TbGd_l13_2.in" "TbGd_l13_3.in" "TbGd_l14_0.in" "TbGd_l14_1.in" "TbGd_l14_2.in" "TbGd_l14_3.in" "TbGd_l15_0.in" "TbGd_l15_1.in" "TbGd_l15_2.in" "TbGd_l15_3.in" "TbGd_l16_0.in" "TbGd_l16_1.in" "TbGd_l16_2.in" "TbGd_l16_3.in" "TbGd_l17_0.in" "TbGd_l17_1.in" "TbGd_l17_2.in" "TbGd_l17_3.in" "TbGd_l18_0.in" "TbGd_l18_1.in" "TbGd_l18_2.in" "TbGd_l18_3.in" "TbGd_l19_0.in" "TbGd_l19_1.in" "TbGd_l19_2.in" "TbGd_l19_3.in" "TbGd_l20_0.in" "TbGd_l20_1.in" "TbGd_l20_2.in" "TbGd_l20_3.in" "TbGd_l21_0.in" "TbGd_l21_1.in" "TbGd_l21_2.in" "TbGd_l21_3.in" "TbGd_l22_0.in" "TbGd_l22_1.in" "TbGd_l22_2.in" "TbGd_l22_3.in" "TbGd_l23_0.in" "TbGd_l23_1.in" "TbGd_l23_2.in" "TbGd_l23_3.in" "TbGd_l24_0.in" "TbGd_l24_1.in" "TbGd_l24_2.in" "TbGd_l24_3.in" "TbGd_l25_0.in" "TbGd_l25_1.in" "TbGd_l25_2.in" "TbGd_l25_3.in" "TbGd_l26_0.in" "TbGd_l26_1.in" "TbGd_l26_2.in" "TbGd_l26_3.in" "TbGd_l27_0.in" "TbGd_l27_1.in" "TbGd_l27_2.in" "TbGd_l27_3.in" "TbGd_l28_0.in" "TbGd_l28_1.in" "TbGd_l28_2.in" "TbGd_l28_3.in" "TbGd_l29_0.in" "TbGd_l29_1.in" "TbGd_l29_2.in" "TbGd_l29_3.in")
for FILE in ${FileList[@]}; do
	python3 "/mnt/c/Users/r0750853/Documents/testGd_layered/create_newlayer_new.py"
	echo python is uitgevoerd 
	
	echo filename is $FILE
	./tridyn2021_linux < $INPUTDIR$FILE

	NAME=$(head -c 10 $INPUTDIR$FILE)
 	ARDN=$"${NAME}_ardn.dat"
	DEPTH_NAMES=$(ls -d ${NAME}_pr*)
	DIR_ARDN=$"Simulated_data/layeredcolorplotmeerr2/Areal_density"
	DIR_DEPTH=$"Simulated_data/layeredcolorplotmeerr2/Depth_profile/${NAME}"
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
