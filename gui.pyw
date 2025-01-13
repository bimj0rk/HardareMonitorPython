import tkinter as tk
from math import sin, cos, radians
import preluator_de_date as pdd

# Helper function to draw a semicircle speedometer
def create_speedometer(canvas, x, y, radius, label, value, max_value=100, is_temp=False):
    # Ensure value is valid
    if value is None or not isinstance(value, (int, float)):
        value = 0

    # Tag for the needle
    needle_tag = f"{label}_needle"

    # Clear previous needle
    canvas.delete(needle_tag)

    # Draw the semicircle
    canvas.create_arc(
        x - radius, y - radius, x + radius, y + radius,
        start=0, extent=180, fill="gray", outline="white", width=2
    )

    # Calculate the needle angle
    angle = 180 - (180 * (value / max_value))

    # Needle coordinates
    needle_length = radius * 0.7
    needle_x = x + needle_length * cos(radians(angle))
    needle_y = y - needle_length * sin(radians(angle))

    # Draw the needle
    canvas.create_line(x, y, needle_x, needle_y, fill="red", width=2, tags=needle_tag)

    return f"{value:.1f}{'°C' if is_temp else '%'}"

# Function to create a category box
def create_category_box(frame, category, data, x, y, box_width, box_height, temp_labels, canvas_dict, label_dict):
    box_frame = tk.Frame(frame, bg="black", width=box_width, height=box_height, relief=tk.RAISED, bd=2)
    box_frame.place(x=x, y=y)

    title_label = tk.Label(box_frame, text=category, font=("Consolas", 14, "bold"), bg="black", fg="white")
    title_label.pack(pady=10)

    canvas = tk.Canvas(box_frame, bg="black", highlightthickness=0, width=box_width, height=box_height - 50)
    canvas.pack()

    # Layout within the category box
    half_height = (box_height - 50) // 2
    radius = 80
    for i, (label, value) in enumerate(data.items()):
        cx = box_width // 2
        cy = half_height // 2 + i * half_height
        is_temp = label in temp_labels
        formatted_value = create_speedometer(canvas, cx, cy, radius, label, value, is_temp=is_temp)
        label_text = canvas.create_text(
            cx, cy + radius + 20, text=f"{label}: {formatted_value}",
            fill="white", font=("Consolas", 12)
        )
        canvas_dict[label] = (canvas, cx, cy, radius, is_temp)
        label_dict[label] = label_text

# Real-time update function
def update_speedometers(canvas_dict, label_dict):
    try:
        # Fetch real-time data
        data = {
            "CPU Temp": pdd.getCpuTemp(),
            "CPU Load": pdd.getCpuLoad(),
            "GPU Temp": pdd.getGpuTemp(),
            "GPU Load": pdd.getGpuLoad(),
            "Motherboard Temp": pdd.getMoboTemp(),  # Added Motherboard Temp
            "RAM Usage": pdd.getMemLoad(),
        }
    except Exception as e:
        print(f"Error fetching data: {e}")
        data = {key: 0 for key in ["CPU Temp", "CPU Load", "GPU Temp", "GPU Load", "Motherboard Temp", "RAM Usage"]}

    # Step 1: Clear previous text
    for label, (canvas, _, _, _, _) in canvas_dict.items():
        canvas.delete(label_dict[label])

    # Step 2: Wait 1 second before updating
    root.after(10, lambda: update_new_data(canvas_dict, label_dict, data))


def update_new_data(canvas_dict, label_dict, data):
    # Step 3: Update speedometers and redraw text
    for label, (canvas, cx, cy, radius, is_temp) in canvas_dict.items():
        formatted_value = create_speedometer(canvas, cx, cy, radius, label, data[label], is_temp=is_temp)
        label_text = canvas.create_text(
            cx, cy + radius + 20, text=f"{label}: {formatted_value}",
            fill="white", font=("Consolas", 12)
        )
        label_dict[label] = label_text

    # Schedule the next update in 3 seconds
    root.after(100, update_speedometers, canvas_dict, label_dict)

# Initialize the GUI
root = tk.Tk()
root.title("System Monitor")
root.geometry("1400x800")
root.configure(bg="black")

# Categories and labels
categories = {
    "CPU": {"CPU Temp": pdd.getCpuTemp(), "CPU Load": pdd.getCpuLoad()},
    "GPU": {"GPU Temp": pdd.getGpuTemp(), "GPU Load": pdd.getGpuLoad()},
    "Motherboard": {"Motherboard Temp": pdd.getMoboTemp(), "RAM Usage": pdd.getMemLoad()},  # Updated
}
temp_labels = {"CPU Temp", "GPU Temp", "Motherboard Temp"}

# Layout
box_width = 400
box_height = 700
x_positions = [50, 500, 950]
canvas_dict = {}
label_dict = {}

# Create boxes for each category
for i, (category, data) in enumerate(categories.items()):
    create_category_box(root, category, data, x_positions[i], 20, box_width, box_height, temp_labels, canvas_dict, label_dict)

# Start updating the GUI
update_speedometers(canvas_dict, label_dict)

# Run the GUI loop
root.mainloop()