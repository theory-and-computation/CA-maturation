import matplotlib.pyplot as plt
import numpy as np

# Function to extract numerical values based on a keyword and position from multiple files
def extract_numeric_values(file_paths, keyword, position):
    values = []
    for file_path in file_paths:
        with open(file_path, "r") as f:
            for line in f:
                if keyword in line:
                    try:
                        parts = line.split()
                        value = float(parts[position])  # Extract number from correct position
                        values.append(value)
                    except (ValueError, IndexError):
                        continue
    return values

# Function to remove outliers using Z-score
def remove_outliers(data, threshold=3.0):
    if len(data) < 2:
        return data  # No filtering needed for very small data

    mean = np.mean(data)
    std_dev = np.std(data)

    filtered_data = [x for x in data if abs((x - mean) / std_dev) < threshold]
    
    return filtered_data

# List of output files to read
file_paths = ["prod1.out", "prod2.out", "prod3.out"]  # Update if needed

# Extract values from all files
density_values = extract_numeric_values(file_paths, "Density", -1)  # Last column
temperature_values = extract_numeric_values(file_paths, "TEMP(K)", 8)  # Column 8
total_energy_values = extract_numeric_values(file_paths, "Etot", 2)  # Third column

# Remove extreme outliers from each dataset
density_values = remove_outliers(density_values)
temperature_values = remove_outliers(temperature_values)
total_energy_values = remove_outliers(total_energy_values)

# Plot all three properties
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].plot(density_values, label="Density", color="blue")
axes[0].set_title("Density")
axes[0].set_xlabel("Time Step")
axes[0].set_ylabel("Density")
axes[0].legend()

axes[1].plot(temperature_values, label="Temperature", color="orange")
axes[1].set_title("Temperature")
axes[1].set_xlabel("Time Step")
axes[1].set_ylabel("Temperature (K)")
axes[1].legend()

axes[2].plot(total_energy_values, label="Total Energy", color="green")
axes[2].set_title("Total Energy")
axes[2].set_xlabel("Time Step")
axes[2].set_ylabel("Energy")
axes[2].legend()

# Print last 10 extracted values to verify correctness
print("Density Values (Last 10, after removing outliers):", density_values[-10:])
print("Temperature Values (Last 10, after removing outliers):", temperature_values[-10:])
print("Total Energy Values (Last 10, after removing outliers):", total_energy_values[-10:])

plt.tight_layout()
plt.show()

