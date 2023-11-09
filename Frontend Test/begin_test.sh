cp -R ../Backend/src/frontend .
open tester.html
dir=$(pwd)
echo "If there's a Command not Found error, open \"$dir\tester.html\" in your browser." 
echo "When you're done testing, press [ENTER]"
read fakevar
rm -rf ./frontend
echo "Testing complete.  Please report any bugs found."