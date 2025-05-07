# Script to simulate user activity to keep Windows session alive and prevent it
# from going to sleep or locking. Moves the mouse slightly at given intervals.
# USAGE: .\Send-SHIFT.ps1

# Add the necessary assembly
Add-Type -AssemblyName System.Windows.Forms

while ($true) {
    # Get the current mouse position
    $pos = [System.Windows.Forms.Cursor]::Position
    Write-Host "Initial mouse position: $pos"

    # Move the mouse slightly
    [System.Windows.Forms.Cursor]::Position = [System.Drawing.Point]::new($pos.X + 1, $pos.Y + 1)
    Start-Sleep -Seconds 1
    [System.Windows.Forms.Cursor]::Position = $pos
    Write-Host "New mouse position: $pos"

    # Wait five minutes (300 seconds) before repeating
    Start-Sleep -Seconds 300
}
