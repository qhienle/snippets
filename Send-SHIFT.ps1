# Script to send "shift" key stroke at interval
# USAGE: .\Send-SHIFT.ps1

# Add the necessary assembly
Add-Type -AssemblyName System.Windows.Forms

# Create a new form (required to use SendKeys)
$form = New-Object System.Windows.Forms.Form

while ($true) {
    # Send the Shift key
    [System.Windows.Forms.SendKeys]::SendWait("+")
    Write-Host "Sent keystroke"
    Start-Sleep -Seconds 300
}
