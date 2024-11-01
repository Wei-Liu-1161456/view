# This file is the entry point of the program. It creates a Company object and a Login object and runs the login screen.
from login import Login
from controller import Company

if __name__ == "__main__":
    company = Company()
    login = Login(company)
    login.run()