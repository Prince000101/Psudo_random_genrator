import time
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def generate_digit_local():
    """
    Generates one pseudo-random digit using only local memory addresses and timestamps.
    """
    obj1 = object()
    obj2 = object()
    total_sum = id(obj1) + time.time_ns() + id(obj2)
    last_two_digits = int(total_sum) % 100
    sum_of_digits = (last_two_digits // 10) + (last_two_digits % 10)
    final_digit = sum_of_digits % 10
    del obj1, obj2
    return final_digit


# --- Data Storage ---
counts = [0] * 10
x_data = []  # Stores the sample number (1, 2, 3...)
y_data = []  # Stores the generated digit
total_samples = 0

# --- Matplotlib Live Visualization Setup ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))


def update(frame):
    """This function is called repeatedly to update both plots."""
    global total_samples

    new_digit = generate_digit_local()

    if new_digit is not None:
        total_samples += 1
        counts[new_digit] += 1
        x_data.append(total_samples)
        y_data.append(new_digit)

    if total_samples == 0: return

    # --- Plot 1: Live Line Plot (Dots Connected) ---
    ax1.clear()
    # This is the changed line: using plot() instead of scatter()
    ax1.plot(x_data, y_data, color='blue', marker='o', linestyle='-')
    ax1.set_title(f'Sequence of Generated Digits (Line Plot)')
    ax1.set_xlabel('Sample Number')
    ax1.set_ylabel('Generated Digit')
    ax1.set_yticks(range(10))
    ax1.set_ylim(-1, 10)
    ax1.set_xlim(0, total_samples + 10)
    # Add a grid for better readability
    ax1.grid(True, linestyle='--', alpha=0.6)

    # --- Plot 2: Live Histogram ---
    ax2.clear()
    digits = [str(i) for i in range(10)]
    ax2.bar(digits, counts, color='mediumpurple')
    average = total_samples / 10.0
    ax2.axhline(y=average, color='r', linestyle='--', label=f'Ideal Average ({average:.1f})')
    ax2.set_title(f'Distribution of Digits (Histogram)')
    ax2.set_xlabel('Generated Digit')
    ax2.set_ylabel('Frequency')
    ax2.set_ylim(0, max(counts) * 1.2 + 1)
    ax2.legend()

    fig.tight_layout()


# Create the animation object.
ani = animation.FuncAnimation(fig, update, interval=100, cache_frame_data=False)

print("🚀 Starting live visualization dashboard... Close the plot window to stop.")
plt.show()