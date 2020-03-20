from openpyxl import Workbook
import requests
import csv


def generate_csv(employee_records):
    """
    Generate CSV File
    """
    records = open('employee_records.csv', 'w')

    with records:
        writer = csv.writer(records)
        writer.writerows(employee_records)

    print(f"[INFO] CSV Generated!")


def csv_to_excel(file_name):
    wb = Workbook()
    ws = wb.active
    with open(file_name, 'r') as f:
        for row in csv.reader(f):
            ws.append(row)
    wb.save(f'employee_records.xlsx')
    print(f'[INFO] Excel File Generated!')


url = "http://dummy.restapiexample.com/api/v1/employees"

employee_records = requests.get(url).json()['data']

record_list = [['id', 'employee_name', 'employee_salary', 'employee_age',
                'profile_image']]
for employee_record in employee_records:
    record_list.append([
        employee_record['id'],
        employee_record['employee_name'],
        employee_record['employee_salary'],
        employee_record['employee_age'],
        employee_record['profile_image']
    ])

generate_csv(record_list)
csv_to_excel('employee_records.csv')
