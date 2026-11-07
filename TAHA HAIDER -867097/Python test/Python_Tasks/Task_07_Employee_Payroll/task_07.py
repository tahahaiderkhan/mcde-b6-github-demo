# Task 07 – Employee Payroll

from abc import ABC, abstractmethod


class Employee(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def calculate_pay(self):
        pass


class SalariedEmployee(Employee):

    def __init__(self, name, salary):
        super().__init__(name)
        self.salary = salary

    def calculate_pay(self):
        return self.salary


class HourlyEmployee(Employee):

    def __init__(self, name, rate, hours):
        super().__init__(name)
        self.rate = rate
        self.hours = hours

    def calculate_pay(self):

        if self.hours > 40:
            overtime = self.hours - 40
            return (40 * self.rate) + (overtime * self.rate * 1.5)

        return self.hours * self.rate


class CommissionEmployee(Employee):

    def __init__(self, name, base, sales, rate):
        super().__init__(name)
        self.base = base
        self.sales = sales
        self.rate = rate

    def calculate_pay(self):
        return self.base + (self.sales * self.rate)


employees = [
    SalariedEmployee("Ali", 50000),
    HourlyEmployee("Ahmed", 20, 45),
    CommissionEmployee("Sara", 500, 4000, 0.10)
]

for emp in employees:
    print(emp.name, "Salary:", emp.calculate_pay())
