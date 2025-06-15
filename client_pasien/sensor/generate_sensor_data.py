import json

data = []
for i in range(3600):
    t = i * 50
    entry = {
        "timestamp": t,
        "position_x": 10 + (i % 5) * 0.01,
        "position_y": 20 + (i % 3) * 0.02,
        "position_z": 5 + (i % 4) * 0.01,
        "force": 0.9 + (i % 10) * 0.005
    }
    data.append(entry)

with open("sensor_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("sensor_data.json generated.")

