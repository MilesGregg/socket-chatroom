#do shell script "python project/Testing.py"
tell application "Terminal"
  activate
  tell application "System Events"
    keystroke "t" using {command down}
  end tell
end tell
