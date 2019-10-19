echo 'Testing call from python...'
python -c 'import Scyland3D; Scyland3D.test_no_regression()'
echo 'Testing call from the command line...'
python Scyland3D.py -i "example/"
python Scyland3D.py -i "example/" -f "upper" -r "36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 37"
python Scyland3D.py -i "example/" -m "upper" -n "identifier,species,location,length,sex,stage,jaw,position,generation"
python -c 'import Scyland3D; Scyland3D._validation_against_ref()'
