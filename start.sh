PORT=9980
if ! [ -z "$1" ]
  then
    PORT=$1
fi

for i in $(eval echo {1..$2})
do
  port=$(expr $i + $PORT)
  python main.py client -p $PORT&
done