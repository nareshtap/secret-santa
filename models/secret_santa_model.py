from dataclasses import dataclass, field
from typing import List, Dict, Any
import random

from services.csv_service import CSVService

class SecretSantaModel:
    def __init__(self, employees: List[Dict[str, Any]] = None, previous_assignments: List[Dict[str, Any]] = None):
        """
        Initialize the Secret Santa Model with employee list and last year's assignments.
        
        Args:
            employees (List[Dict[str, Any]]): List of current employees participating.
            previous_assignments (List[Dict[str, Any]]): List of previous year's assignments.
        """
        self.employees = employees if employees is not None else []
        self.last_year_assignments = previous_assignments if previous_assignments is not None else []
        self.result: List[Dict[str, Any]] = []

    def load_employees_from_csv(self, file_path: str):
        """
        Reads employee data from a CSV file, validates it, and stores it in the model.
        
        Args:
            file_path (str): Path to the CSV file.
            
        Raises:
            ValueError: If validation fails.
            Exception: If file reading fails.
        """
        try:
            data = CSVService.read_csv(file_path)
            
            if not data:
                raise ValueError("The CSV file is empty.")

            if len(data) <= 2:
                raise ValueError("The number of employees must be more than 2 for Secret Santa.")

            seen_emails = set()
            for i, row in enumerate(data, start=1):
                name = row.get('Employee_Name')
                email = row.get('Employee_EmailID')
                
                if not name or not name.strip():
                    raise ValueError(f"'Employee_Name' is missing or empty at row {i}.")
                
                if not email or not email.strip():
                    raise ValueError(f"'Employee_EmailID' is missing or empty at row {i}.")
                
                if email in seen_emails:
                    raise ValueError(f"Duplicate email found: '{email}' at row {i}.")
                seen_emails.add(email)
                
            self.employees = data

        except Exception as e:
            raise e


    def load_last_year_assignments(self, file_path: str):
        """
        Reads last year's assignment data from a CSV file, validates it, and stores it in the model.
        
        Args:
            file_path (str): Path to the CSV file.
            
        Raises:
            ValueError: If validation fails.
            Exception: If file reading fails.
        """
        try:
            data = CSVService.read_csv(file_path)
            
            if not data:
                print("Warning: Last year's assignment file is empty.")
                self.last_year_assignments = []
                # It's okay if last year's data is empty, just warn and continue
                return

            for i, row in enumerate(data, start=1):
                emp_name = row.get('Employee_Name')
                emp_email = row.get('Employee_EmailID')
                child_name = row.get('Secret_Child_Name')
                child_email = row.get('Secret_Child_EmailID')
                
                if not emp_name or not emp_name.strip():
                    raise ValueError(f"'Employee_Name' is missing or empty in last year's assignment file at row {i}.")
                
                if not emp_email or not emp_email.strip():
                    raise ValueError(f"'Employee_EmailID' is missing or empty in last year's assignment file at row {i}.")

                if not child_name or not child_name.strip():
                    raise ValueError(f"'Secret_Child_Name' is missing or empty in last year's assignment file at row {i}.")

                if not child_email or not child_email.strip():
                    raise ValueError(f"'Secret_Child_EmailID' is missing or empty in last year's assignment file at row {i}.")
                
            self.last_year_assignments = data

        except Exception as e:
            raise e

    def generate_assignments(self):
        """
        Generates Secret Santa assignments based on the provided logic.
        Stores the result in self.result.
        
        Raises:
            ValueError: If there are not enough participants.
            RuntimeError: If a valid assignment cannot be found.
        """
        employees = self.employees
        n = len(employees)
        if n < 2:
            raise ValueError("Need at least 2 participants") 
        
        # Map email to employee dict for easy lookup
        email_to_emp = {e['Employee_EmailID']: e for e in employees}
        
        # Working with emails as unique identifiers
        names = [e['Employee_EmailID'] for e in employees]
        
        # Build last year map: email -> email
        last_year = {}
        for row in self.last_year_assignments:
            giver = row.get('Employee_EmailID')
            child = row.get('Secret_Child_EmailID')
            if giver and child:
                last_year[giver] = child
                
        receivers = names[:]
        receivers = names[:]
        
        # Retry logic: Try to find a valid permutation multiple times
        max_attempts = 100
        for attempt in range(max_attempts):
            random.shuffle(receivers)
            
            # Step 1: Remove self-assignments (Greedy Swaps)
            for i in range(n):
                if names[i] == receivers[i]:
                    j = (i + 1) % n
                    receivers[i], receivers[j] = receivers[j], receivers[i]

            # Step 2: Fix last-year repeats (Greedy Swaps)
            valid_assignment = True
            for i in range(n):
                if last_year.get(names[i]) == receivers[i]:
                    # Need to swap with someone else, j
                    possible_swap_found = False
                    for j in range(n):
                        if (
                            names[j] != receivers[j] and           # j is not self-assigned
                            receivers[j] != names[i] and           # j's current receiver for i is okay (checks self-assignment for i)
                            receivers[i] != names[j] and           # i's current receiver for j is okay (checks self-assignment for j)
                            last_year.get(names[j]) != receivers[i] and # i's current receiver for j is okay (checks last year for j)
                            last_year.get(names[i]) != receivers[j]     # j's current receiver for i is okay (checks last year for i)
                        ):
                            receivers[i], receivers[j] = receivers[j], receivers[i]
                            possible_swap_found = True
                            break
                    if not possible_swap_found:
                        valid_assignment = False
                        break
            
            # Additional Check: Ensure absolutely no constraints are violated after swaps
            if valid_assignment:
                final_check_pass = True
                for i in range(n):
                    if names[i] == receivers[i]:
                        final_check_pass = False
                        break
                    if last_year.get(names[i]) == receivers[i]:
                        final_check_pass = False
                        break
                
                if final_check_pass:
                    # Build result and return
                    self.result = []
                    for giver_email, child_email in zip(names, receivers):
                        giver_data = email_to_emp[giver_email]
                        child_data = email_to_emp[child_email]
                        
                        self.result.append({
                            'Employee_Name': giver_data['Employee_Name'],
                            'Employee_EmailID': giver_data['Employee_EmailID'],
                            'Secret_Child_Name': child_data['Employee_Name'],
                            'Secret_Child_EmailID': child_data['Employee_EmailID']
                        })
                    return

        # If loop completes without return
        raise RuntimeError("No valid Secret Santa assignment exists after multiple attempts.")
        

    def run(self):
        """
        Entry point for the Secret Santa process.
        """
        try:
            # 1. Load Employees
            employee_file = input("Enter the path to the Employee CSV file: ").strip()
            self.load_employees_from_csv(employee_file)

            # 2. Load Last Year's Assignments
            previous_file = input("Enter the path to last year's assignment CSV file (optional, press Enter to skip): ").strip()
            if previous_file:
                 self.load_last_year_assignments(previous_file)
            else:
                self.last_year_assignments = []
                print("No previous year's file provided. Proceeding without constraints from last year.")

            # 3. Generate Assignments
            self.generate_assignments()

            # 4. Save Results
            output_file = input("Enter the path to save the result CSV file (default: secret_santa_result.csv): ").strip()
            if not output_file:
                output_file = "secret_santa_result.csv"
            if not output_file:
                output_file = "secret_santa_result.csv"
            # Removed raw print(self.result) for better UX
            
            CSVService.write_csv(output_file, self.result)
            print(f"Results successfully saved to {output_file}")

        except Exception as e:
            print(e)
