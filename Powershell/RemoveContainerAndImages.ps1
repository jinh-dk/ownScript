<#
    write the container name in argments, will remove all the container, and its image
#>

foreach ($arg in $args) 
{
    RemoveContainterAndImage.ps1 $arg
}