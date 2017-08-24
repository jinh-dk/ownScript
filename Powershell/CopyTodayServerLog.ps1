param(
    [string]$dest = "server"
)

$d = Get-Date -Format yyyyMMdd
if ($dest -eq "server")
{
    docker cp docker_server_1:/app/src/Publishing.Server/logs/log-$d.txt . 
}
if ($dest -eq "api")
{
    docker cp docker_api_1:/app/src/Publishing.Api/logs/log-$d.txt . 
}