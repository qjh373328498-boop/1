# Convert-BatFiles.ps1
# PowerShell script to convert UTF-8 .bat files to ANSI (GBK)

$files = @(
    "软件/启动菜单.bat",
    "软件/软件启动工具/一键启动-Windows 系统.bat",
    "软件/Windows 安装包/启动菜单.bat",
    "软件打包工具/一键打包-Windows.bat"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        # Read UTF-8 content
        $content = Get-Content -Path $file -Raw -Encoding UTF8
        # Write as GBK (GB2312)
        $encoding = [System.Text.Encoding]::GetEncoding(936)
        [System.IO.File]::WriteAllText($file, $content, $encoding)
        Write-Host "Converted: $file" -ForegroundColor Green
    } else {
        Write-Host "Not found: $file" -ForegroundColor Yellow
    }
}

Write-Host "`nAll files converted to ANSI (GBK)!" -ForegroundColor Green
Write-Host "Now you can run the .bat files in Windows CMD." -ForegroundColor Cyan
