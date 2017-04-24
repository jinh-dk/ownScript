echo "Port number $1"
lsof -n -i4TCP:$1 | grep LISTEN