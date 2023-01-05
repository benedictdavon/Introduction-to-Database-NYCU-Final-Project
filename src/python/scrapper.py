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
# ########## For Undergraduate Courses ##########
# for choosing what semester we want, for now we don't use it
# select_semester = driver.find_element(By.ID, "fAcySem")

# # selecting the undergraduate course in the timetable
# select_type = Select(driver.find_element(By.ID, "fType"))
# type_undergrad = select_type.select_by_index(0)

# # get all colleges that are available
# select_colleges = Select(driver.find_element(By.ID, "fCollege"))
# colleges = select_colleges.options

# # only get the department in Chiao Tung Campus
# colleges = colleges[7:] 

# # loop through every college option
# for college in colleges:
#     # get the college name
#     college_name = college.get_attribute('innerText')
#     temp = {}

#     # select the college name in the web
#     select_colleges.select_by_value(college.get_attribute("value"))

#     # add pause to wait for the web to change
#     time.sleep(2)

#     # get all departments that are available
#     select_department = Select(driver.find_element(By.ID, "fDep"))
#     departments = select_department.options
#     for department in departments:
#         department_name = department.get_attribute('innerText')

#         Select(driver.find_element(By.ID, "fGroup")).select_by_index(0)
#         Select(driver.find_element(By.ID, "fGrade")).select_by_index(0)
#         Select(driver.find_element(By.ID, "fClass")).select_by_index(0)

#         time.sleep(1)
#         button = driver.find_element(By.ID, "crstime_search")
#         button.click()
#         time.sleep(1)

#         temp[department_name] = []

#         tables = driver.find_elements(By.CLASS_NAME, "table_list")
#         print(len(tables))
#         for t in range(len(tables)):
#             path = "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr"
#             rows = 1 + len(driver.find_elements(By.XPATH, path))
#             for row in range(3, rows+1):
#                 course = {}

#                 if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]") == False:
#                     continue

#                 course['id']       = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]").get_attribute('innerText')
#                 course['c_name']   = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[6]").get_attribute('innerText')
#                 course['code']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[3]").get_attribute('innerText')
#                 course['name']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]").get_attribute('innerText')
#                 course['limit']    = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[7]").get_attribute('innerText')
#                 course['reg']      = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[8]").get_attribute('innerText')
#                 course['time']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[9]").get_attribute('innerText')
#                 course['credit']   = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[10]").get_attribute('innerText')
#                 course['hours']    = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[11]").get_attribute('innerText')
#                 course['teacher']  = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[12]").get_attribute('innerText')
#                 course['type']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[13]").get_attribute('innerText')

#                 temp[department_name].append(course)
#                 print(department_name, course)

#     undergraduate_course[college_name] = temp

########## For Common Required Course for Undergraduate ##########
# selecting the undergraduate course in the timetable
select_type = Select(driver.find_element(By.ID, "fType"))
common_undergraduate = select_type.select_by_index(2)

time.sleep(2)

select_category = Select(driver.find_element(By.ID, "fCategory"))
common_req_undergraduate = select_category.select_by_index(0)

# get all colleges that are available
select_sections = Select(driver.find_element(By.ID, "fDep"))
sections = select_sections.options

def key_exist_inside_dict_values(dict, key):
    for value in dict.values():
        if key in value.keys():
            return False

    return True

print(len(sections))

common_required_undergraduate = {}
# loop through every college option
for section in sections:
    # get the college name
    section_name = section.get_attribute('innerText')
    temp = {}

    # select the college name in the web
    select_sections.select_by_value(section.get_attribute("value"))

    # add pause to wait for the web to change
    time.sleep(2)

    button = driver.find_element(By.ID, "crstime_search")
    button.click()
    time.sleep(12)

    tables = driver.find_elements(By.CLASS_NAME, "table_list")

    for t in range(1, len(tables)+1):
        path = "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr"
        rows = 1 + len(driver.find_elements(By.XPATH, path))
        path =  "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/caption"
        department_name = driver.find_element(By.XPATH, path).get_attribute('innerText')
        department_name = department_name[1:department_name.index("》")]
        if department_name not in temp.keys():
            temp[department_name] = []

        for row in range(3, rows+1):
            
            if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]") == False:
                if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td"):
                    course['memo'] = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td").get_attribute('innerText')
                    course = {}
                    temp[department_name].append(course)
                    continue
        
                continue
        
            course = {}
            temp[department_name].append(course)

            course['id']       = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]").get_attribute('innerText')
            course['c_name']   = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[6]").get_attribute('innerText')
            course['code']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[3]").get_attribute('innerText')
            course['summary']  = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[4]").get_attribute('innerText')
            course['name']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]").get_attribute('innerText')
            course['limit']    = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[7]").get_attribute('innerText')
            course['reg']      = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[8]").get_attribute('innerText')
            course['time']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[9]").get_attribute('innerText')
            course['credit']   = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[10]").get_attribute('innerText')
            course['hours']    = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[11]").get_attribute('innerText')
            course['teacher']  = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[12]").get_attribute('innerText')
            course['type']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[13]").get_attribute('innerText')
            print(department_name, course)
        if temp == None:
            print("temp is none")
    common_required_undergraduate[section_name] = temp

########## For Common Required Course in College ##########

select_category = Select(driver.find_element(By.ID, "fCategory"))
common_req_undergraduate = select_category.select_by_index(1)

time.sleep(2)

# get all colleges that are available
select_sections = Select(driver.find_element(By.ID, "fDep"))
sections = select_sections.options

def key_exist_inside_dict_values(dict, key):
    for value in dict.values():
        if key in value.keys():
            return False

    return True

print("total dept: ", len(sections))

common_required_undergraduate = {}
# loop through every college option
for section in sections:
    # get the college name
    section_name = section.get_attribute('innerText')
    temp = {}

    # select the college name in the web
    select_sections.select_by_value(section.get_attribute("value"))

    # add pause to wait for the web to change
    time.sleep(2)

    button = driver.find_element(By.ID, "crstime_search")
    button.click()
    time.sleep(12)

    tables = driver.find_elements(By.CLASS_NAME, "table_list")

    for t in range(1, len(tables)+1):
        path = "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr"
        rows = 1 + len(driver.find_elements(By.XPATH, path))
        path =  "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/caption"
        department_name = driver.find_element(By.XPATH, path).get_attribute('innerText')
        department_name = department_name[1:department_name.index("》")]
        if department_name not in temp.keys():
            temp[department_name] = []

        for row in range(3, rows+1):
            
            if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]") == False:
                if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td"):
                    course['memo'] = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td").get_attribute('innerText')
                    course = {}
                    temp[department_name].append(course)
                    continue
        
                continue
        
            course = {}
            temp[department_name].append(course)

            course['id']       = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]").get_attribute('innerText')
            course['c_name']   = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[6]").get_attribute('innerText')
            course['code']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[3]").get_attribute('innerText')
            course['summary']  = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[4]").get_attribute('innerText')
            course['name']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]").get_attribute('innerText')
            course['limit']    = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[7]").get_attribute('innerText')
            course['reg']      = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[8]").get_attribute('innerText')
            course['time']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[9]").get_attribute('innerText')
            course['credit']   = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[10]").get_attribute('innerText')
            course['hours']    = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[11]").get_attribute('innerText')
            course['teacher']  = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[12]").get_attribute('innerText')
            course['type']     = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[13]").get_attribute('innerText')
            print(department_name, course)
        if temp == None:
            print("temp is none")
    common_required_undergraduate[section_name] = temp

for value in common_required_undergraduate.values():
    print(value)

with open(r"C:\Users\Davon\Desktop\University\Semester 3\Introduction to Database System\Final Project\common_required.json", "w", encoding='utf-8') as outfile:
    json.dump(common_required_undergraduate, outfile, indent = 4, sort_keys = False, ensure_ascii=False)

