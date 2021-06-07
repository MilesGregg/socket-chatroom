echo "Hello"

#osascript -e 'tell app "Terminal"
#   do script "echo hello"
#end tell'

#osascript -e "tell application \"Terminal\" to do script (container of (path to me)) \"python3 Testing.py\""


function new() {
    if [[ $# -eq 0 ]]; then
        open -a "Terminal" "$PWD"
    else
        open -a "Terminal" "$@"
    fi
}

new Testing.py
