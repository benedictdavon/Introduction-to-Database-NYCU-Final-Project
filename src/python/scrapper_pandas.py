import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# our website URL
url = "https://timetable.nycu.edu.tw/?flang=en-us"
driver = webdriver.Chrome()

# we only get the courses for undergraduate courses and common required courses for undergraduate for now
cols_name = ['semester', 'college', 'department', 'id', 'code', 'memo', 'name', 'chinese_name', 'limit', 'reg_num', 'time', 'credit', 'hours', 'lecturer',' type']
undergrad_df = pd.DataFrame(columns=cols_name)

common_req_columns = ['semester', 'college', 'department', 'id', 'code', 'name', 'chinese_name', 'limit', 'reg_num', 'time', 'credit', 'hours', 'lecturer',' type']
common_req_df = pd.DataFrame(columns=cols_name)

driver.get(url)
time.sleep(5)
########## For Undergraduate Courses ##########
semesters = ['1111', '1112']
select_semester = Select(driver.find_element(By.ID, "fAcySem"))

def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


for semester in semesters:
    print(semester)
    select_semester.select_by_value(semester)
    time.sleep(1)
    
    # selecting the undergraduate course in the timetable
    select_type = Select(driver.find_element(By.ID, "fType"))
    type_undergrad = select_type.select_by_index(0)

    # get all colleges that are available
    select_colleges = Select(driver.find_element(By.ID, "fCollege"))
    colleges = select_colleges.options

    # only get the department in Chiao Tung Campus
    colleges = colleges[7:] 
    # loop through every college option
    for college in colleges:
        # get the college name
        college_name = college.get_attribute('innerText')
        college_name = college.get_attribute('innerText')
        temp = {}

        # select the college name in the web
        select_colleges.select_by_value(college.get_attribute("value"))

        # add pause to wait for the web to change
        time.sleep(2)

        # get all departments that are available
        select_department = Select(driver.find_element(By.ID, "fDep"))
        departments = select_department.options
        for department in departments:
            department_name = department.get_attribute('innerText')

            Select(driver.find_element(By.ID, "fGroup")).select_by_index(0)
            Select(driver.find_element(By.ID, "fGrade")).select_by_index(0)
            Select(driver.find_element(By.ID, "fClass")).select_by_index(0)

            time.sleep(1.5)
            button = driver.find_element(By.ID, "crstime_search")
            button.click()
            time.sleep(3)

            tables = driver.find_elements(By.CLASS_NAME, "table_list")
            print(len(tables))
            for t in range(len(tables)):
                path = "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr"
                rows = 1 + len(driver.find_elements(By.XPATH, path))
                course = {'college':college_name, 'department':department_name}
                for row in range(3, rows+1):
                    if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]") == False:
                        continue

                    if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]") == False:
                        if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td"):
                            course['memo'] = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td").get_attribute('innerText')
                            undergrad_df=undergrad_df.append(course)
                            print(course)
                            course = {'college':college_name, 'department':department_name}
                            continue
                        continue

                    undergrad_df=undergrad_df.append(course, ignore_index=True)
                    print(course)
                    course = {'college':college_name, 'department':department_name}

                    course['semester']      = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[1]").get_attribute('innerText')
                    course['id']            = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]").get_attribute('innerText')
                    course['chinese_name']  = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[6]").get_attribute('innerText')
                    course['code']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[3]").get_attribute('innerText')
                    course['name']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]").get_attribute('innerText')
                    xpath = "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]/span"
                    if check_exists_by_xpath(xpath):
                        spanLength = len(driver.find_elements(By.XPATH, xpath))
                        for span in range(1, spanLength+1):
                            spanText = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]/span["+ str(span) +"]").get_attribute('innerText')
                            course['name'] = course['name'].replace(spanText, '')
                    course['limit']         = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[7]").get_attribute('innerText')
                    course['reg_num']       = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[8]").get_attribute('innerText')
                    course['time']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[9]").get_attribute('innerText')
                    course['credit']        = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[10]").get_attribute('innerText')
                    course['hours']         = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[11]").get_attribute('innerText')
                    course['lecturer']      = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[12]").get_attribute('innerText')
                    course['type']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[13]").get_attribute('innerText')

print(undergrad_df.head)
undergrad_df.to_csv(r"C:\Users\Davon\Desktop\University\Semester 3\Introduction to Database System\Final Project\src\dataset\undergraduate_courses.csv", encoding='utf-8-sig')

######### For Common Required Course for Undergraduate ##########
# selecting the undergraduate course in the timetable
for semester in semesters:
    select_semester.select_by_value(semester)
    time.sleep(1)
    select_type = Select(driver.find_element(By.ID, "fType"))
    common_undergraduate = select_type.select_by_index(2)

    time.sleep(2)

    select_category = Select(driver.find_element(By.ID, "fCategory"))
    common_req_undergraduate = select_category.select_by_index(0)

    # get all colleges that are available
    select_sections = Select(driver.find_element(By.ID, "fDep"))
    sections = select_sections.options

    # loop through every college option
    for section in sections:
        # get the college name
        section_name = section.get_attribute('innerText')

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
            course = {'college':section_name, 'department':department_name}
            for row in range(3, rows+1):
                
                if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]") == False:
                    if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td"):
                        course['memo'] = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td").get_attribute('innerText')
                        common_req_df = common_req_df.append(course, ignore_index=True)
                        course = {'college':section_name, 'department':department_name}
                        continue
            
                    continue
            
                common_req_df = common_req_df.append(course, ignore_index=True)
                course = {'college':section_name, 'department':department_name}

                course['semester']      = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[1]").get_attribute('innerText')
                course['id']            = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]").get_attribute('innerText')
                course['chinese_name']  = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[6]").get_attribute('innerText')
                course['code']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[3]").get_attribute('innerText')
                course['name']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]").get_attribute('innerText')
                xpath = "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]/span"
                if check_exists_by_xpath(xpath):
                        spanLength = len(driver.find_elements(By.XPATH, xpath))
                        for span in range(1, spanLength+1):
                            spanText = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]/span["+ str(span) +"]").get_attribute('innerText')
                course['limit']         = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[7]").get_attribute('innerText')
                course['reg_num']       = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[8]").get_attribute('innerText')
                course['time']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[9]").get_attribute('innerText')
                course['credit']        = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[10]").get_attribute('innerText')
                course['hours']         = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[11]").get_attribute('innerText')
                course['lecturer']      = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[12]").get_attribute('innerText')
                course['type']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[13]").get_attribute('innerText')
                
                print(department_name, course)

    ########## For Common Required Course in College ##########
    select_category = Select(driver.find_element(By.ID, "fCategory"))
    common_req_undergraduate = select_category.select_by_index(1)

    time.sleep(2)

    # get all colleges that are available
    select_sections = Select(driver.find_element(By.ID, "fDep"))
    sections = select_sections.options
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
            for row in range(3, rows+1):
                
                if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]") == False:
                    if check_exists_by_xpath("/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td"):
                        course['memo'] = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td").get_attribute('innerText')
                        common_req_df = common_req_df.append(course, ignore_index=True)
                        print(course)
                        course = {'college':section_name, 'department':department_name}
                        continue
            
                    continue
            
                common_req_df = common_req_df.append(course, ignore_index=True)
                print(course)
                course = {'college':section_name, 'department':department_name}

                course['id']            = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[2]").get_attribute('innerText')
                course['chinese_name']  = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[6]").get_attribute('innerText')
                course['code']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[3]").get_attribute('innerText')
                course['summary']       = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[4]").get_attribute('innerText')
                course['name']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]").get_attribute('innerText')
                xpath = "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]/span"
                if check_exists_by_xpath(xpath):
                        spanLength = len(driver.find_elements(By.XPATH, xpath))
                        for span in range(1, spanLength+1):
                            spanText = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[5]/span["+ str(span) +"]").get_attribute('innerText')
                course['limit']         = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[7]").get_attribute('innerText')
                course['reg_num']       = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[8]").get_attribute('innerText')
                course['time']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[9]").get_attribute('innerText')
                course['credit']        = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[10]").get_attribute('innerText')
                course['hours']         = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[11]").get_attribute('innerText')
                course['lecturer']      = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[12]").get_attribute('innerText')
                course['type']          = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/table[" + str(t) + "]/tbody/tr[" + str(row) + "]/td[13]").get_attribute('innerText')
            
print(common_req_df.head)

common_req_df.to_csv(r"C:\Users\Davon\Desktop\University\Semester 3\Introduction to Database System\Final Project\src\dataset\common_undergrad_courses.csv", encoding='utf-8-sig')
