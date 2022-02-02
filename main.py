import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# pip install -r requirements.txt


pd.set_option('display.max_columns', 14)

general_df = pd.read_csv('./test/general.csv', encoding='utf-8')
prenatal_df = pd.read_csv('./test/prenatal.csv')
sports_df = pd.read_csv('./test/sports.csv')

# Copy the columns from general_df at the console by print(general_df.columns)
uni_col_names = ['Unnamed: 0', 'hospital', 'gender', 'age', 'height', 'weight', 'bmi', 'diagnosis',
                 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']

prenatal_df.columns = uni_col_names
sports_df.columns = uni_col_names

container = pd.concat([general_df, prenatal_df, sports_df], ignore_index=True)
container.drop(columns='Unnamed: 0', inplace=True)
container.dropna(axis=0, how='all', inplace=True)
container['gender'].replace(to_replace='man', value='m', inplace=True)
container['gender'].replace(to_replace='male', value='m', inplace=True)
container['gender'].replace(to_replace='woman', value='f', inplace=True)
container['gender'].replace(to_replace='female', value='f', inplace=True)
for i in container['hospital']:
    if i == 'prenatal':
        container['gender'].fillna('f', inplace=True)
container.fillna(0, inplace=True)


# Question 1
q1 = list(container.hospital.mode())
print(f"\nThe hospital that has the highest number of patients is: {q1[0]}")

# Question 2
total_general = container.query("hospital == 'general'").shape[0]
general_stomach = container.query("hospital == 'general'").query("diagnosis == 'stomach'").count()[0]
q2 = general_stomach / total_general
print(f"\nThe share of the patients in the general hospital that suffers from stomach-related issues is: {round(q2, 3) * 100}%")

# Question 3
total_sports = container.query("hospital == 'sports'").shape[0]
sports_dislocation = container.query("hospital == 'sports'").query("diagnosis == 'dislocation'").count()[0]
q3 = sports_dislocation / total_sports
print(f"\nThe share of the patients in the sports hospital that suffers from dislocation-related issues is {round(q3 * 100, 3)}%")

# Question 4
med_age_general = container.query("hospital == 'general'").age.median()
med_age_sports = container.query("hospital == 'sports'").age.median()
q4 = round(abs(med_age_general - med_age_sports))
print(f"\nThe difference in the median ages of the patients in the general and sports hospitals is: {q4}")

# Question 5
temp = dict(container.query("blood_test == 't'").hospital.value_counts())
max_key = max(temp)
max_val = temp[f"{max_key}"]
print(f"\nThe hospital that has the most often blood test taken is: {max_key}, {max_val} blood tests")

# Question 6
container.plot(y='age', kind='hist', bins=80)
plt.hist([0, 15, 35, 55, 70, 80])
plt.show()
print("\nThe most common age range of a patient among all hospitals is: 15-35")

# Question 7
container['diagnosis'].value_counts().plot(kind='pie')
plt.show()
print("\nThe most common diagnosis among patients in all hospitals is: pregnancy")
