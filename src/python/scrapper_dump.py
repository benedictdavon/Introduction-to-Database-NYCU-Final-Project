import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# our website URL
url = "https://timetable.nycu.edu.tw/?flang=en-us"
driver = webdriver.Chrome()

# function to check if element exist by XPATH
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

# we only get the courses for undergraduate courses and common required courses for undergraduate for now
undergraduate_course = {}
common_required_undergraduate = {}
# semester = {}

driver.get(url)
time.sleep(5)

# for choosing what semester we want, for now we don't use it
# select_semester = driver.find_element(By.ID, "fAcySem")

# selecting the undergraduate course in the timetable
select_type = Select(driver.find_element(By.ID, "fType"))
type_undergrad = select_type.select_by_index(0)

# selecting the colleges
select_colleges = Select(driver.find_element(By.ID, "fCollege"))
# get all colleges that are available
colleges = select_colleges.options
# only get the department in Chiao Tung Campus
colleges = colleges[7:] 

# while True:   # repeat until the try statement succeeds
#     try:
#         myfile = open(r"C:\Users\Davon\Desktop\University\Semester 3\Introduction to Database System\Final Project\undergraduate.json") # or "a+", whatever you need
#         print("file opened!")
#         break                             # exit the loop
#     except IOError:
#         input("Could not open file! Please close Excel. Press Enter to retry.")
#         # restart the loop
        
# with myfile:
#     pass

for college in colleges:
    college_name = college.get_attribute('innerText')
    temp = {}

    select_colleges.select_by_value(college.get_attribute("value"))

    time.sleep(2)
    select_department = Select(driver.find_element(By.ID, "fDep"))
    departments = select_department.options
    for department in departments:
        department_name = department.get_attribute('innerText')

        Select(driver.find_element(By.ID, "fGroup")).select_by_index(0)
        Select(driver.find_element(By.ID, "fGrade")).select_by_index(0)
        Select(driver.find_element(By.ID, "fClass")).select_by_index(0)

        time.sleep(1)
        button = driver.find_element(By.ID, "crstime_search")
        button.click()
        time.sleep(1)

        temp[department_name] = []

        tables = driver.find_elements(By.CLASS_NAME, "table_list")
        print(len(tables))
        for t in range(len(tables)):
            path = "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr"
            rows = 1 + len(driver.find_elements(By.XPATH, path))
            for row in range(3, rows+1):
                course = {}

                if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]") == False:
                    continue

                cos_id          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]").get_attribute('innerText')
                cos_other_name  = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[6]").get_attribute('innerText')
                cos_code        = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[3]").get_attribute('innerText')
                cos_name        = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]").get_attribute('innerText')
                cos_num_limit   = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[7]").get_attribute('innerText')
                cos_reg_num     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[8]").get_attribute('innerText')
                cos_time        = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[9]").get_attribute('innerText')
                cos_credit      = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[10]").get_attribute('innerText')
                cos_hours       = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[11]").get_attribute('innerText')
                cos_teacher     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[12]").get_attribute('innerText')
                cos_type        = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[13]").get_attribute('innerText')

                course['id']      = cos_id
                course['c_name']  = cos_other_name
                course['code']    = cos_code
                course['name']    = cos_name
                course['limit']   = cos_num_limit
                course['reg']     = cos_reg_num
                course['time']    = cos_time
                course['credit']  = cos_credit
                course['hours']   = cos_hours
                course['teacher'] = cos_teacher
                course['type']    = cos_type
                temp[department_name].append(course)
                print(department_name, course)

    undergraduate_course[college_name] = temp

with open(r"C:\Users\Davon\Desktop\University\Semester 3\Introduction to Database System\Final Project\undergraduate.json", "w") as outfile:
    json.dump(undergraduate_course, outfile, indent = 4, sort_keys = False)

        # for table in tables:
        #     tr = table.find_element(By.TAG_NAME, "tr")
        #     rows = table.find_elements(By.NAME, "tr_three_char")
        #     print('Rows:', len(rows))
        #     for row in rows:
        #         course = {}
        #         cos_id          = row.find_element(By.NAME, "cos_id").get_attribute('innerText')
        #         cos_other_name  = row.find_element(By.NAME, "cos_othername").get_attribute('innerText')
        #         cos_code        = row.find_element(By.NAME, "cos_code").get_attribute('innerText')
        #         cos_name        = row.find_element(By.NAME, "cos_name").get_attribute('innerText')
        #         cos_num_limit   = row.find_element(By.NAME, "num_limit").get_attribute('innerText')
        #         cos_reg_num     = row.find_element(By.NAME, "reg_num").get_attribute('innerText')
        #         cos_time        = row.find_element(By.NAME, "cos_time").get_attribute('innerText')
        #         cos_credit      = row.find_element(By.NAME, "cos_credit").get_attribute('innerText')
        #         cos_hours       = row.find_element(By.NAME, "cos_hours").get_attribute('innerText')
        #         cos_type        = row.find_element(By.NAME, "cos_type").get_attribute('innerText')
        #         cos_teacher     = row.find_element(By.NAME, "teacher").get_attribute('innerText')

        #         course['id']      = cos_id
        #         course['c_name']  = cos_other_name
        #         course['code']    = cos_code
        #         course['name']    = cos_name
        #         course['limit']   = cos_num_limit
        #         course['reg']     = cos_reg_num
        #         course['time']    = cos_time
        #         course['credit']  = cos_credit
        #         course['hours']   = cos_hours
        #         course['type']    = cos_type
        #         course['teacher'] = cos_teacher
        #         temp[department_name].append(course)
        #         print(department_name, course)

        # undergraduate_course[college_name] = temp
        # for key, value in undergraduate_course.items():
        #     print(key, ': ', value)
