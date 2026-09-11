import numpy as np
import pandas as pd

# Part 1 : Charging and exploring dataset
df = pd.read_csv("employees2.csv") # charging the csv file employees2.csv
print(df.head(10)) # displaying the first ten lines
print(df.dtypes) # showing the types of each column
print(df.isna().sum()) # printing the missing values count of each column

# Part 2 : Data cleaning
df["Age"] = df["Age"].fillna(df["Age"].median())# filling the missing values in column 'Age' with median
df["Salary"] = df["Salary"].fillna(df.groupby("Department")["Salary"].transform("mean"))# filling the missing values in column Salary with the mean of salary for each department
df = df.astype({"Age":int,"Salary":float,"Years_Experience":int})# converting the age and years_experience to type int
df["Remote"] = np.where(df["Remote"] == "Yes","Oui","Non")# Replacing the values in remote column Yes/No with Oui/Non
# creating a new column that classes the years of expertize
bins = [0,3,8,15,100]
labels = ['Junior','Intermédiaire','Senior','Expert']
df["Ancienneté_Catégorie"] = pd.cut(df["Years_Experience"],bins=bins,labels=labels,include_lowest=True)

#Part 3 : Analyzes explore and statistics
average_salary = df["Salary"].mean()# calculating the average salary
most_payed_employee = df[df["Salary"] == df["Salary"].max()]# finding the most paying employee
average_salary_department = df.groupby('Department')["Salary"].mean()# calculating the average salary by department
mean_median_by_expertize_group = df.groupby('Ancienneté_Catégorie')["Salary"].agg(["mean","median"])# calculating the average and median salary by seniority categories
remote_count_by_department = df.groupby('Department')["Remote"].agg("count")# remote employee count by department

#Part 4 : Pivot Tables
pt = df.pivot_table(
            values="Salary",
            index="Department",
            columns="Remote",
            aggfunc="mean"
        )# pivot table created that shows average salary per department and remote
# creating a new column that classes the age
bins = [0,18,60,100]
labels = ["Child","Adult","Senior"]
df["grouped_aged"] = pd.cut(df["Age"],bins=bins,labels=labels)
avg_seniority = df.pivot_table(values="Years_Experience",index="grouped_aged",columns="Department",aggfunc="mean")# pivot table created that shows average expertize years per age groups and department

#Part 5 : Advanced calculations with numpy
df["Performance"] = np.where(df["Salary"] <60000,"Bon",np.where(df["Salary"] < 80000,"Moyen","Haut"))# using np.where() to create a column
conditions = [
    (df['Age'] < 35) & (df['Years_Experience'] < 5),
    (df['Age'] < 35) & (df['Years_Experience'] >= 5),
    (df['Age'] >= 35) & (df['Years_Experience'] < 5),
    (df['Age'] >= 35) & (df['Years_Experience'] >= 5)
]
choices = ["Jeune & Nouveau","Jeune & Expérimenté","Senior & Nouveau","Senior & Expérimenté"]
df["Categorie"] = np.select(conditions,choices,default="Non classe")# using np.select() to create a column
salary_difference = df["Salary"] - df.groupby("Department")["Salary"].transform("mean")# calculating the difference between salary and average salary per department