<#
    .DESCRIPTION
        Stop a docker service, rebuild the image, and start with new image.
#>

Param(
    [string]$dockerservice,
    [string]$folder
)

if ($folder) 
{
    cd $folder
}

docker-compose.exe -f .\docker-compose-dbs.yml -f .\docker-compose-full.yml stop $dockerservice
docker-compose.exe -f .\docker-compose-dbs.yml -f .\docker-compose-full.yml build $dockerservice
docker-compose.exe -f .\docker-compose-dbs.yml -f .\docker-compose-full.yml start $dockerservice