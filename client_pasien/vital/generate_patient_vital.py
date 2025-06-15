import json

data = []
for i in range(3600):
    t = i * 50
    entry = {
        "timestamp": t,
        "heart_rate": 75 + (i % 5),
        "blood_pressure_systolic": 120 + (i % 3),
        "blood_pressure_diastolic": 80 + (i % 2),
        "oxygen_saturation": 98 + (i % 2)
    }
    data.append(entry)

with open("patient_data.hl7.json", "w") as f:
    json.dump(data, f, indent=2)

print("patient_data.hl7.json generated.")
