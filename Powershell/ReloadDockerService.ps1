<#
    .DESCRIPTION
        Stop a docker service, rebuild the image, and start with new image.
#>

Param(
    [string]$dockerservice,
    [string]$folder = $null    
)

if ($folder) 
{
    cd $folder
}

docker-compose.exe -f .\docker-compose-dbs.yml -f .\docker-compose-full.yml stop $dockerservice
#docker-compose.exe -f .\docker-compose-dbs.yml -f .\docker-compose-full.yml build --pull --force-rm $dockerservice 
docker-compose.exe -f .\docker-compose-dbs.yml -f .\docker-compose-full.yml create --build $dockerservice 
# Sometimes I see start the new images, even the file in the container from new image, but the behaviour is still like old image.
# So try remove the unused image before start the serviced again.
RemoveUnusedImages.ps1
docker-compose.exe -f .\docker-compose-dbs.yml -f .\docker-compose-full.yml start $dockerservice
