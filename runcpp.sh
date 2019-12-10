set -e

DAY=`printf %02d $1`

g++ day${DAY}.cpp --std=c++17 && ./a.out
rm a.out