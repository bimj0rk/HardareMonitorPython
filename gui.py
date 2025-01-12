import tkinter as tk
from math import sin, cos, radians

# Helper function to draw a semicircle speedometer
def create_speedometer(canvas, x, y, radius, label, value, max_value=100):
    # Draw the semicircle
    canvas.create_arc(
        x - radius, y - radius, x + radius, y + radius,
        start=0, extent=180, fill="gray", outline="white", width=2
    )

    # Correct angle calculation
    angle = 180 - (180 * (value / max_value))  # Map value to angle, 180° to 0°

    # Calculate needle end coordinates
    needle_length = radius * 0.7  # Adjusted needle length
    needle_x = x + needle_length * cos(radians(angle))
    needle_y = y - needle_length * sin(radians(angle))  # Subtract y to point upward

    # Draw the needle
    canvas.create_line(x, y, needle_x, needle_y, fill="red", width=2)

    # Add label and value text below the speedometer
    canvas.create_text(x, y + radius + 5, text=f"{label}: {value}%", fill="white", font=("Consolas", 12))

# Function to create a category box
def create_category_box(frame, category, data, x, y, box_width, box_height):
    box_frame = tk.Frame(frame, bg="black", width=box_width, height=box_height, relief=tk.RAISED, bd=2)
    box_frame.place(x=x, y=y)
    
    title_label = tk.Label(box_frame, text=category, font=("Consolas", 14, "bold"), bg="black", fg="white")
    title_label.pack(pady=10)

    canvas = tk.Canvas(box_frame, bg="black", highlightthickness=0, width=box_width, height=box_height - 50)
    canvas.pack()

    # Divide the box into two halves
    half_height = (box_height - 50) // 2
    radius = 80
    for i, (label, value) in enumerate(data.items()):
        cx = box_width // 2
        cy = half_height // 2 + i * half_height  # Center within each half
        create_speedometer(canvas, cx, cy, radius, label, value)

# Initialize GUI
root = tk.Tk()
root.title("System Monitor")
root.geometry("1400x800")  # Increased height for better spacing
root.configure(bg="black")

# Static data for demonstration
categories = {
    "CPU": {"CPU Temp": 55, "CPU Load": 45},
    "GPU": {"GPU Temp": 65, "GPU Load": 35},
    "RAM": {"RAM Usage": 60},
}

# Create category boxes
box_width = 400
box_height = 700  # Adjusted box height for better proportions
x_positions = [50, 500, 950]  # Adjusted X-coordinates for the three columns

for i, (category, data) in enumerate(categories.items()):
    create_category_box(root, category, data, x_positions[i], 20, box_width, box_height)

# Run the GUI
root.mainloop()
