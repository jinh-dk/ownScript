$d = Get-Date -Format yyyyMMdd
docker cp docker_server_1:/app/src/Publishing.Server/logs/log-$d.txt . 