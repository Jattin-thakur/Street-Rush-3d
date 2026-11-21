import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('monthly_marks.csv')
dff = pd.read_csv('students_marks.csv')
print(df)
x = [11,65,62,54]
y = [1,2,5,15]
plt.plot(x, y)
subject = ['Maths', 'Science', 'English', 'History']


# Create a plot
plt.plot(x, y, label='Sine Wave')
plt.title('Simple Plot')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.legend()
plt.grid(True)
plt.scatter(x, y, color='red', label='Data Points')
plt.bar(subject, x, color='blue', label='Marks')
plt.title('Marks Distribution')
plt.xlabel('Subjects')
plt.ylabel('Marks')

plt.show()