import re

message = "19a.168.46"
print(bool(re.match("^[0-9\.]*$", message)))

