import numpy as np
import matplotlib.pyplot as plt

def solve_qho(N, L_max=5.0):
    """Solves the Quantum Harmonic Oscillator for a given grid size N."""
    dx = (2 * L_max) / (N + 1)
    x = np.linspace(-L_max + dx, L_max - dx, N)
    V = 0.5 * x**2
    t = 1.0 / (2 * dx**2)
    
    diag = np.full(N, 2 * t) + V
    off = np.full(N - 1, -t)
    H = np.diag(diag) + np.diag(off, k=1) + np.diag(off, k=-1)
    
    E, vecs = np.linalg.eigh(H)
    psi = vecs / np.sqrt(dx)
    return x, dx, E, psi

# 1. Normalisation and Error Calculation for a fixed grid (N=500)
x, dx, E, psi = solve_qho(500)
print("--- Wavefunction Normalisation ---")
for n in range(3):
    norm = np.sum(psi[:, n]**2) * dx
    print(f"State n={n} norm: {norm:.6f}")

print("\n--- Numerical Errors (N=500) ---")
for n in range(3):
    E_exact = n + 0.5
    error = abs(E[n] - E_exact)
    print(f"State n={n}: E_num = {E[n]:.6f}, E_exact = {E_exact:.1f}, Error = {error:.2e}")

# 2. Grid Convergence Analysis
N_values = [50, 100, 200, 400, 800, 1600]
dx_values = []
errors_E0 = []

for N in N_values:
    _, dx_curr, E_curr, _ = solve_qho(N)
    dx_values.append(dx_curr)
    errors_E0.append(abs(E_curr[0] - 0.5))  # Error against ground state E=0.5

# Setup plots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot A: Convergence
axes[0].loglog(dx_values, errors_E0, 'bo-', label='Numerical Error')
axes[0].loglog(dx_values, [dx**2 for dx in dx_values], 'k--', label=r'$\mathcal{O}(\Delta x^2)$ Reference')
axes[0].set_xlabel("Grid Spacing (dx)")
axes[0].set_ylabel("Absolute Error in Ground State Energy")
axes[0].set_title("Grid Convergence Analysis")
axes[0].legend()
axes[0].grid(True, which="both", ls="--", alpha=0.5)

# Plot B: Eigenfunction Comparison
# Analytical ground state: pi^(-1/4) * exp(-x^2 / 2)
psi_0_exact = (1.0 / np.pi)**0.25 * np.exp(-0.5 * x**2)
p = psi[:, 0]
if p[np.argmax(np.abs(p))] < 0: 
    p = -p # Fix arbitrary phase

axes[1].plot(x, p, 'bo', markersize=3, label="Numeric n=0")
axes[1].plot(x, psi_0_exact, 'r-', lw=2, label="Analytical n=0", alpha=0.7)
axes[1].set_xlabel("x")
axes[1].set_ylabel(r"$\psi_0(x)$")
axes[1].set_title("Eigenfunction: Numeric vs Analytical")
axes[1].legend()

plt.tight_layout()
plt.savefig("convergence_results.png", dpi=150)
plt.show()