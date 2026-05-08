import csv
#coloms
sal_col = 4
age_col = 3
exp_years_col = 5
emp_id_col = 0
name_col = 1
dept_col = 2

def read_csv():
    filename = "employees.csv"
    while True:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                return list(reader)
        except FileNotFoundError:
            print("CSV file not found.")
            filename = input("Enter valid csv file : ")

def summary_numeric(lines):
    tot_salary = 0
    #tmp_val = lines[0].split(",")
    min_sal = None
    max_sal = None
    line_cnt = 0
    for line in lines :            
        try :
            salary = float(line[sal_col])
            #print(salary)
            if min_sal == None :
                min_sal = salary
            if max_sal == None :
                max_sal = salary
            if (salary > max_sal) : 
                max_sal = salary
            if (salary < min_sal) :
                min_sal = salary
            #print ("Max : ", max_sal, "Min : ", min_sal)
            tot_salary = tot_salary + salary
            line_cnt = line_cnt + 1
        except ValueError:
            print ("Bad value")
    print ("Total : ", tot_salary, "\nAverage : ", tot_salary / line_cnt)
    print ("Max : ", max_sal, "\nMin : ", min_sal)


def dept_wise_count(lines):
    counts = {}
    for line in lines :
        dept = line[dept_col]
        counts[dept] = counts.get(dept, 0) + 1
    return counts

def summary_data(lines):
    print("Rows : ", len(lines)-1)
    print("Coloms:" , len(lines[0]))
    print("Headers : ", lines[0])

if __name__ == "__main__":
    lines = read_csv()
    #lines = read_file()
    if len(lines) > 0 :
        summary_data(lines)
    
    if len(lines) <= 1 :
        print("File has no records of data")
    else :
        lines = lines[1:]
        summary_numeric(lines)
        print(dept_wise_count(lines))
