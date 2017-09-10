path="$1"
sum="$2"

if [ -z "$sum"]; then
    du -hcsk "$path"
else
    du -h "$path"
fi

