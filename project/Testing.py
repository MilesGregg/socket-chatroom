message = "[SENDTO:ALL:john]=hi"
name = message.split("]")[0][1:].split(":")[2] + ": "
print(name)

