import requests
import datetime
import time
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# --- Your Random Number Generation Logic (from your script) ---
def generate_digit(api_key):
    """
    Generates one pseudo-random digit using the Weather API and returns it.
    """
    cities = ["London", "Paris", "New York", "Tokyo", "Sydney", "Delhi", "Cairo", "Moscow", "Rio de Janeiro", "Beijing"]
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    try:
        temp_var_id = id(object())
        id_last_digit = temp_var_id % 10
        selected_city = cities[id_last_digit % len(cities)]

        params = {'q': selected_city, 'appid': api_key, 'units': 'metric'}
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()

        temperature = weather_data['main']['temp']
        weather_data_id = id(weather_data)
        current_timestamp = datetime.datetime.now().timestamp()
        total_sum = temperature + weather_data_id + current_timestamp
        last_two_digits = int(total_sum) % 100
        sum_of_digits = (last_two_digits // 10) + (last_two_digits % 10)
        final_digit = sum_of_digits % 10
        return final_digit
    except requests.exceptions.RequestException:
        return None


# --- Data Storage for Both Plots---
API_KEY = "81851fabdb4567bd8748aa7e3541d47c"
counts = [0] * 10
x_data = []  # For the line plot's x-axis
y_data = []  # For the line plot's y-axis
total_samples = 0

# --- Matplotlib Live Visualization Setup ---
# Create a figure with two subplots (axes) side-by-side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))


def update(frame):
    """This function is called repeatedly to update both plots."""
    global total_samples

    new_digit = generate_digit(API_KEY)

    if new_digit is not None:
        # Update data for both plots
        total_samples += 1
        counts[new_digit] += 1
        x_data.append(total_samples)
        y_data.append(new_digit)

    if total_samples == 0: return

    # --- Plot 1: Live Line Plot (Dots Connected) ---
    ax1.clear()
    ax1.plot(x_data, y_data, color='black', marker='o', linestyle='-')
    ax1.set_title(f'Sequence of Generated Digits (Line Plot)')
    ax1.set_xlabel('Sample Number')
    ax1.set_ylabel('Generated Digit')
    ax1.set_yticks(range(10))
    ax1.set_ylim(-1, 10)
    ax1.set_xlim(0, total_samples + 10)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # --- Plot 2: Live Histogram ---
    ax2.clear()
    digits = [str(i) for i in range(10)]
    ax2.bar(digits, counts, color='blue')
    average = total_samples / 10.0
    ax2.axhline(y=average, color='r', linestyle='--', label=f'Ideal Average ({average:.1f})')
    ax2.set_title(f'Distribution of Digits (Histogram)')
    ax2.set_xlabel('Generated Digit')
    ax2.set_ylabel('Frequency')
    ax2.set_ylim(0, max(counts) * 1.2 + 1)
    ax2.legend()

    # Improve overall layout
    fig.tight_layout()


# Create the animation object.
ani = animation.FuncAnimation(fig, update, interval=500, cache_frame_data=False)

print("🚀 Starting live visualization... Close the plot window to stop.")
plt.show()

print("\n--- Final Distribution ---")
for i, count in enumerate(counts):
    percentage = (count / total_samples * 100) if total_samples > 0 else 0
    print(f"Digit {i}: Appeared {count} times ({percentage:.2f}%)")