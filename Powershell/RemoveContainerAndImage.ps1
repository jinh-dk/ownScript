<#
    .DESCRIPTION
        Remove the container and its image. 
        If the image is used by other containers too, other containers will also be removed.
    .DEPENDENCY
        Powershell Docker module.
        https://github.com/Microsoft/Docker-PowerShell
#>

Param (
    [string]$name
)

Write-Host "Stop and remove container $name"

Stop-Container $name
$image = (Get-Container -ContainerIdOrName $name).Image
Remove-Container $name

# Looking for other container which also use this image
$other_container = (Get-Container | Where-Object {$_.Image -eq $image}).Names
Write-Host "Stop and remove container $other_container"
Stop-Container $other_containers
Remove-Container $other_container

Write-Host "Remove image $image"
Remove-ContainerImage $image