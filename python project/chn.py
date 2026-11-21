import tkinter as tk
from tkinter import messagebox
def calculate_nutrients():
    try:
        age = int(age_entry.get())
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        gender = gender_var.get()

        if age < 1 or age > 50:
            messagebox.showerror("Invalid Age", "Enter an age between 1 and 18.")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror("Invalid Input", "Weight and height must be positive.")
            return

        if age <= 3:
            calories = weight * 90
            protein = weight * 1.05
            calcium = 700
            iron = 7
            water = weight * 100

        elif age <= 8:
            calories = weight * 75
            protein = weight * 0.95
            calcium = 1000
            iron = 10
            water = weight * 70

        elif age <= 13:
            calories = weight * 60
            protein = weight * 0.95
            calcium = 1300
            iron = 8
            water = weight * 55

        else:
            calories = weight * 45
            protein = weight * 0.85
            calcium = 1300
            iron = 11 if gender == "Male" else 15
            water = weight * 40
        carbohydrates = (calories * 0.55) / 4
        fats = (calories * 0.30) / 9

        # BMI
        height_m = height / 100
        bmi = weight / (height_m ** 2)

        result = f"""
Child Nutrient Requirements
----------------------------

Age: {age} years
Gender: {gender}
Weight: {weight:.1f} kg
Height: {height:.1f} cm

Estimated Daily Requirements:

Calories     : {calories:.0f} kcal
Protein      : {protein:.1f} g
Carbohydrates: {carbohydrates:.1f} g
Fat          : {fats:.1f} g
Calcium      : {calcium} mg
Iron         : {iron} mg
Water        : {water:.0f} ml

BMI: {bmi:.1f}
"""

        result_label.config(text=result)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for age, weight and height."
        )
root = tk.Tk()
root.title("Child Nutrients Calculator")
root.geometry("550x650")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Child Nutrients Calculator",
    font=("Arial", 22, "bold")
)
title.pack(pady=20)
tk.Label(root, text="Age (years)", font=("Arial", 12)).pack()
age_entry = tk.Entry(root, font=("Arial", 12))
age_entry.pack(pady=5)
tk.Label(root, text="Gender", font=("Arial", 12)).pack(pady=(10, 0))

gender_var = tk.StringVar(value="Male")

gender_frame = tk.Frame(root)
gender_frame.pack()

tk.Radiobutton(
    gender_frame,
    text="Male",
    variable=gender_var,
    value="Male"
).pack(side="left", padx=10)

tk.Radiobutton(
    gender_frame,
    text="Female",
    variable=gender_var,
    value="Female"
).pack(side="left", padx=10)

tk.Label(root, text="Weight (kg)", font=("Arial", 12)).pack(pady=(10, 0))
weight_entry = tk.Entry(root, font=("Arial", 12))
weight_entry.pack(pady=5)

tk.Label(root, text="Height (cm)", font=("Arial", 12)).pack(pady=(10, 0))
height_entry = tk.Entry(root, font=("Arial", 12))
height_entry.pack(pady=5)

calculate_button = tk.Button(
    root,
    text="Calculate Nutrients",
    font=("Arial", 12, "bold"),
    command=calculate_nutrients
)
calculate_button.pack(pady=20)

result_label = tk.Label(
    root,
    text="Enter the child's details and click Calculate.",
    font=("Arial", 11),
    justify="left",
    anchor="w"
)
result_label.pack(padx=30, pady=10)

root.mainloop()