Param (
    [string]$folder="C:\\Users\\jinxu\\Documents\\GitHub\\kunai\\master\\docker"
)

$container = Get-Container | Where-Object {$_.Names -like "*docker_kallithea_1*"}
if (($container.ID -eq $null) -or $container.Status.Contains("Exited")) {
    Push-Location $folder
    Write-Host "Restart Kallithea Container"
    docker-compose.exe -f docker-compose-dbs.yml up --force-recreate kallithea     
} else {
    Write-Host "Container "  $container.ID  " is found and running."
}

Pop-Location