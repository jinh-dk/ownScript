<#
    Create the test document from test script.
#>

param(
    [string]$folder,
    [string]$outputfilename,
    [string]$filetype = "cs"
)

Push-Location $outputfilename
$files = (Get-ChildItem . -Filter '*.$filetype' | Select-Object -ExpandProperty Name)
foreach ($file in $files)
{
    $lines = Get-Content $file
    foreach($line in $lines)
    {
        if( $line -match '.*public\s+.+Test\(.+' ) 
        {
            # Write-Test name
        }

        if($line -match '////\s*[Ss]tep\s+:')
        {
            # Write-Test Step

        }
    }
}


