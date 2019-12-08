set -e

DAY=`printf %02d $1`

g++ day${DAY}.cpp && ./a.out
rm a.out