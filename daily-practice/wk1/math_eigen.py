import numpy as np
import json

# Define a 3x3 matrix
A = np.array([[4, 1, 2], [1, 3, 0], [2, 0, 5]])

# Calculate eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

print(f"Matrix:\n{A}")
print(f"\nEigenvalues:\n{eigenvalues}")
print(f"\nEigenvectors:\n{eigenvectors}")

# Verify A * v = lambda * v
v = eigenvectors[:, 0]      # First eigenvector
lam = eigenvalues[0]        # First eigenvalue
left_side = A @ v
right_side = lam * v
print(f"\nVerification (A*v == lambda*v): {np.allclose(left_side, right_side)}")

for i in range(3):
    v = eigenvectors[:, i]
    lam = eigenvalues[i]
    print(f"λ={lam:.3f}  Av==λv? {np.allclose(A @ v, lam * v)}")