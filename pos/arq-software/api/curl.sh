PAYLOAD=`curl -X POST -H "Content-Type: application/json" -d "{\"user\": \"abc\"}" "http://127.0.0.1:5000/token"`
TOKEN=`echo $PAYLOAD | python3 -m json.tool | sed -n -e '/"token":/ s/^.*"\(.*\)".*/\1/p'`
curl -X POST -H "Authentication: $TOKEN" -F "file=@./file.csv" "http://127.0.0.1:5000/upload"