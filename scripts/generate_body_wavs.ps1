param(
    [string]$InputPath = "./script.md",
    [string]$OutputDir = "./generated/body_wavs",
    [string]$Voice = "af_sarah",
    [string]$Lang = "en-us",
    [double]$Speed = 0.96
)

$ErrorActionPreference = "Stop"

function Resolve-FullPath {
    param(
        [string]$BasePath,
        [string]$CandidatePath
    )

    if ([System.IO.Path]::IsPathRooted($CandidatePath)) {
        return [System.IO.Path]::GetFullPath($CandidatePath)
    }

    return [System.IO.Path]::GetFullPath((Join-Path $BasePath $CandidatePath))
}

function Convert-ToWslPath {
    param([string]$WindowsPath)

    $fullPath = [System.IO.Path]::GetFullPath($WindowsPath)

    if ($fullPath -match '^([A-Za-z]):\\?(.*)$') {
        $drive = $matches[1].ToLowerInvariant()
        $rest = $matches[2] -replace '\\', '/'
        if ([string]::IsNullOrWhiteSpace($rest)) {
            return "/mnt/$drive"
        }
        return "/mnt/$drive/$rest"
    }

    throw "Unsupported path for WSL conversion: $fullPath"
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$windowsInputPath = Resolve-FullPath -BasePath $repoRoot -CandidatePath $InputPath
$windowsOutputDir = Resolve-FullPath -BasePath $repoRoot -CandidatePath $OutputDir

$wslRepoRoot = Convert-ToWslPath -WindowsPath $repoRoot
$wslInputPath = Convert-ToWslPath -WindowsPath $windowsInputPath
$wslOutputDir = Convert-ToWslPath -WindowsPath $windowsOutputDir

$bashCommand = @(
    "cd '$wslRepoRoot'"
    "scripts/generate_body_wavs.sh '$wslInputPath' '$wslOutputDir' --voice '$Voice' --lang '$Lang' --speed '$Speed'"
) -join "; "

wsl.exe bash -lc $bashCommand
