from ZODB import DB
from ZODB.FileStorage import FileStorage
from ZODB.PersistentMapping import PersistentMapping
import persistent
import transaction

class Employee(persistent.Persistent):

    def __init__(self, name, manager=None):
        self.name=name
        self.manager=manager

#  Configurando la base de datos
storage=FileStorage("./storage/employees.fs")
db=DB(storage)
connection=db.open()
root=connection.root()



#  Crea un mammping vacio si es necesario
keys = root.keys()

if 'employees' not in keys:
    root['employees']={}
    transaction.commit()

employees=root["employees"]

def listEmployees():
    if len(employees.values())==0:
        print("There are no employees.")
        return
    for employee in employees.values():
        print("-----------------------")
        print(f"Name : {employee.name}")
        if employee.manager is not None:
            print(f"Manager's name: : {employee.manager.name}")
        

def addEmployee(name, manager_name=None):
    if name in employees:
        print("Employee already exists.")
        return
    if manager_name is not None:
        try:
            manager=employees[manager_name]
        except KeyError:
            print("Manager does not exist.")
            return

        employees[name]=Employee(name, manager)
    else:
        employees[name]=Employee(name)

    root['employees']=employees
    transaction.commit()
    print("Employee added.")


def deleteEmployee(name):
    if name not in employees:
        print("Employee does not exist.")
        return
    del employees[name]
    root['employees']=employees
    transaction.commit()
    print("Employee deleted.")

def editEmploye(name):
    if name not in employees:
        print("Employee does not exist.")
        return
    print("Enter new name:")
    new_name=input()
    employees[name].name=new_name
    root['employees']=employees
    transaction.commit()
    print("Employee edited.")

#Add employees
addEmployee("John")
addEmployee("Mary","John")
addEmployee("Mike","John")

#List employees
print("***List of employees after add:***")
listEmployees()

#Delete employee
deleteEmployee("Mike")

print("***List of employees after delete:***")
listEmployees()


