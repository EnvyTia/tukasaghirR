import numpy as np
import json
import os

# -------------------------------
# KONFIGURASI & INISIALISASI
# -------------------------------

# Jumlah pengguna (eMBB/URLLC) dan resource block
U = 3   # Jumlah user
B = 5   # Jumlah Resource Block

# Prioritas trafik (θ): URLLC lebih tinggi dari eMBB
theta_urllc = 0.7
theta_embb = 0.3

# Inisialisasi status neuron: semua RB awalnya untuk eMBB (1 = eMBB, 0 = URLLC)
v = np.ones((U, B))

# Bobot koneksi antar neuron (acak untuk simulasi awal)
w = np.random.uniform(0.1, 1.0, size=(U, B, U, B))

# Ambang batas antar neuron
theta = np.full((U, B), theta_embb)
theta[0] = theta_urllc  # Misal: user 0 adalah URLLC

# Energi awal
energy_prev = float('inf')

# -------------------------------
# FUNGSI ENERGI & UPDATE
# -------------------------------

def calculate_energy(v, w, theta):
    energy = 0
    for i in range(U):
        for j in range(B):
            for k in range(U):
                for l in range(B):
                    energy -= 0.5 * w[i][j][k][l] * v[i][j] * v[k][l]
            energy += theta[i][j] * v[i][j]
    return energy

def update_neurons(v, w, theta):
    v_new = v.copy()
    for i in range(U):
        for j in range(B):
            total_input = 0
            for k in range(U):
                for l in range(B):
                    total_input += w[i][j][k][l] * v[k][l]
            v_new[i][j] = 1 if total_input >= theta[i][j] else 0
    return v_new

# -------------------------------
# ITERASI SAMPAI KONVERGENSI
# -------------------------------

max_iter = 100
for iteration in range(max_iter):
    v = update_neurons(v, w, theta)
    energy_curr = calculate_energy(v, w, theta)
    print(f"Iterasi {iteration}: Energi = {energy_curr:.4f}")
    if abs(energy_prev - energy_curr) < 1e-3:
        print("Konvergen.")
        break
    energy_prev = energy_curr

# -------------------------------
# SIMPAN OUTPUT KE JSON
# -------------------------------

rb_allocation = v.astype(int).tolist()  # ubah ke list integer

# Buat folder output jika belum ada
os.makedirs("output", exist_ok=True)

with open("output/rb_allocation.json", "w") as f:
    json.dump({"rb_allocation": rb_allocation}, f, indent=2)

print("\nHasil alokasi RB telah disimpan ke output/rb_allocation.json")
