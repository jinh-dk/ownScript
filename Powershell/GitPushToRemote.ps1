#Param(
#    [string] $commitmessage
#)

if ($args.Count -eq 0 )
{
    Write-Host "Commit message is madatory"
    break;
} elseif ($args.Count -ge 2) {
    Write-Host "Too many arguments, only 1 is allowed."
    break;
}


$branch = git branch
if ($branch -contains '* master') {
    Write-Host "you are on master branch, which push is not allowed by this script."
    break;
}

Write-Host " Push the changes..."
git add .
git commit $commitmessage
git push