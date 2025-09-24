import pandas as pd

students = pd.read_csv("data/students.csv")
internships = pd.read_csv("data/internships.csv")

print(students.head())
print(internships.head())
