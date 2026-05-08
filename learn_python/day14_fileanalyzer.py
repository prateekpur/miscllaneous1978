import csv
#coloms
sal_col = 4
age_col = 3
exp_years_col = 5
emp_id_col = 0
name_col = 1
dept_col = 2
REQUIRED_FIELDS = {"Salary", "Department"}

def read_csv():
    filename = "employees.csv"
    while True:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                 # --- Schema validation ---
                if reader.fieldnames is None:
                    print("Invalid file: No header found.")
                    continue

                missing_fields = REQUIRED_FIELDS - set(reader.fieldnames)

                if missing_fields:
                    print("Invalid CSV schema!")
                    print("Missing columns:", missing_fields)
                    print("Found columns:", reader.fieldnames)
                    filename = input("Enter valid csv file: ")
                    continue

                return list(reader), reader.fieldnames
        except FileNotFoundError:
            print("CSV file not found.")
            filename = input("Enter valid csv file : ")

def summary_numeric(lines):
    tot_salary = 0
    #tmp_val = lines[0].split(",")
    min_sal = float("inf")
    max_sal = float("-inf")
    line_cnt = 0
    for line in lines :            
        try :
            salary = float(line["Salary"])
            #print(salary)
            if (salary > max_sal) : 
                max_sal = salary
            if (salary < min_sal) :
                min_sal = salary
            tot_salary = tot_salary + salary
            line_cnt += 1
        except (ValueError, KeyError):
            print ("Bad value")
    if line_cnt == 0:
        print("No valid salary data found.")
        return 0, 0, 0, 0
    return tot_salary, tot_salary / line_cnt, max_sal, min_sal


def dept_wise_count(lines):
    counts = {}
    for line in lines :
        try :

            dept = line["Department"]
            counts[dept] = counts.get(dept, 0) + 1
        except KeyError:
            continue
    return counts

def summary_data(lines):
    return len(lines), len(lines[0]) 

if __name__ == "__main__":
    lines, header = read_csv()
    if header != None :
        print("Header : ", header)
    #lines = read_file()
    if len(lines) > 0 :
       row, col = summary_data(lines)
       print("Rows : " , row, "\nColoms : ", col)
    
    if len(lines) <= 1 :
        print("File has no records of data")
    else :
        tot_salary, avg_salary, max_sal, min_sal = summary_numeric(lines)
        print ("Total Sal : " , tot_salary, "\nAverage Sal : ", avg_salary, 
               "\nMax Salary : ", max_sal, " \nMin Salary : ", min_sal)
        print(dept_wise_count(lines))
