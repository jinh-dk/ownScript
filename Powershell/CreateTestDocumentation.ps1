<#
    Create the test document from test script.
#>

param(
    [string]$folder,
    [string]$outputfilename,
    [string]$filetype = "cs"
)

Push-Location $folder
$files = (Get-ChildItem . -Filter "*.$filetype" | Select-Object -ExpandProperty Name)
Write-Host $files
foreach ($file in $files)
{
    Write-Host $file
    $lines = Get-Content $file
    foreach($line in $lines)
    {
        if( $line -match '.*public\s+.+Test\(.+' -or $line -match '////\s*[Ss]tep\s+:') 
        {
            # Write-Test name
            $content += $line
            $content += ' `n '  
        }
    }
}
Pop-Location
$content | Set-Content $outputfilename


