import json

data = []
commands = ["move_forward", "move_left", "move_right", "rotate", "move_backward"]

for i in range(3600):
    t = i * 50
    entry = {
        "timestamp": t,
        "command": commands[i % len(commands)],
        "speed": 1.0 + (i % 3) * 0.1,
        "angle": (i % 10) * 5.0  # rotasi sudut
    }
    data.append(entry)

with open("control_commands.json", "w") as f:
    json.dump(data, f, indent=2)

print("control_commands.json generated.")
