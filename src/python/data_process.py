import pandas as pd

undergrad = pd.read_csv(r"C:\Users\Davon\Desktop\University\Semester 3\Introduction to Database System\Final Project\src\dataset\undergraduate_courses.csv")
undergrad = undergrad.dropna(subset=['course_id'])
colleges = sorted(undergrad['college'].unique())

columns = undergrad.columns[1:]

departments = sorted(undergrad['department'].unique())
department_df = pd.DataFrame(columns=['code', 'name', 'full'])
for department in departments:
    code = department[:3]
    name = department[4:-1]
    department_df = department_df.append({'code':code, 'name':name, 'full':department}, ignore_index = True)

undergrad['department'] = undergrad['department'].replace(department_df['full'].tolist(), department_df['code'].tolist())
undergrad.drop_duplicates(subset='course_id',inplace=True)

undergrad['type'] = undergrad['type'].replace({"Required": 1, "Elective": 2, "Core curriculum": 3, "Physical Education": 4, "Language & communication":5})
# for some reason there's a \xa0 instead of  ' ' in semester field
undergrad['semester'] = undergrad['semester'].replace({"111\xa0Fall Semester": 1111, "111\xa0Spring Semester": 1112}) 
# if it's in the course registration period, the reg_num is displayed as '-', which we don't want
undergrad['reg_num'] = undergrad['reg_num'].replace({'-':0})
# remove the last char of every value in name column because original data contains a '\n'
undergrad['name'] = undergrad['name'].apply(lambda x: x[:-1] if x[-1] == '\n' else x)

undergrad = undergrad.drop(columns=['college'])
undergrad = undergrad.drop(columns=['department'])
columns = undergrad.columns[1:]
print(undergrad.head)

undergrad.to_csv(f"C:\\Users\\Davon\\Desktop\\University\\Semester 3\\Introduction to Database System\\Final Project\\src\\dataset\\undergraduate_updated.csv", columns=columns, encoding='utf-8-sig', index=False)

##### Common Required For Undergraduate #####
common_undergrad = pd.read_csv(r"C:\Users\Davon\Desktop\University\Semester 3\Introduction to Database System\Final Project\src\dataset\common_undergrad_courses.csv")
# Removing rows that are don't have course id
common_undergrad = common_undergrad.dropna(subset=['course_id'])

colleges = sorted(common_undergrad['college'].unique())

columns = common_undergrad.columns[1:]

# departments = sorted(common_undergrad['department'].unique())
department_df = pd.DataFrame(columns=['code', 'name', 'full'])
for department in departments:
    code = department[:3]
    name = department[4:-1]
    department_df = department_df.append({'code':code, 'name':name, 'full':department}, ignore_index = True)

common_undergrad['department'] = common_undergrad['department'].replace(department_df['full'].tolist(), department_df['code'].tolist())
common_undergrad.drop_duplicates(subset='course_id',inplace=True)

common_undergrad['type'] = common_undergrad['type'].replace({"Required": 1, "Elective": 2, "Core curriculum": 3, "Physical Education": 4, "Language & communication":5})
common_undergrad['semester'] = common_undergrad['semester'].replace({"111\xa0Fall Semester": 1111, "111\xa0Spring Semester": 1112})
common_undergrad['reg_num'] = common_undergrad['reg_num'].replace({'-':0})
common_undergrad['name'] = common_undergrad['name'].apply(lambda x: x[:-1] if x[-1] == '\n' else x)

common_undergrad = common_undergrad.drop(columns=['college'])
common_undergrad = common_undergrad.drop(columns=['department'])
columns = common_undergrad.columns[1:]

common_undergrad.to_csv(f"C:\\Users\\Davon\\Desktop\\University\\Semester 3\\Introduction to Database System\\Final Project\\src\\dataset\\common_undergrad_updated.csv", columns=columns, encoding='utf-8-sig', index=False)

# Merge two file
courses = pd.concat([common_undergrad, undergrad])

courses.drop_duplicates(subset='course_id',inplace=True)
courses.to_csv(f"C:\\Users\\Davon\\Desktop\\University\\Semester 3\\Introduction to Database System\\Final Project\\src\\dataset\\courses.csv", columns=columns, encoding='utf-8-sig', index=False)