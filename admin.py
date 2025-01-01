from datetime import date
from typing import List, Dict, Optional, Any
from auth import AuthenticationManager, AuthCLI
from users import User

class User:
    def __init__(self, user_id: str, name: str, email: str, password: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

class Admin(User):
    """
    Concrete implementation of the User class for Admins.
    """
    @classmethod
    def create_admin(cls, email: str, password: str, auth_manager: AuthenticationManager):
        """Create a new admin account."""
        success, message = auth_manager.register(email, password, role='admin')
        if success:
            return cls(user_id=email, name=email.split('@')[0], email=email, password=password)
        else:
            print(message)
            return None

    def __init__(self, user_id: str, name: str, email: str, password: str, access_level: str = "Admin", department: str = None):
        # Ensure that the access_level is passed directly to the User constructor
        super().__init__(user_id, name, email, password)
        # Set access level and department
        self.access_level = access_level
        self.department = department  # Add department attribute

    def get_user_details(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "access_level": self.access_level,
            "department": self.department  # Include department in user details
        }

    def update_user_details(self, name: str = None, email: str = None, password: str = None, access_level: str = None, department: str = None):
        if name:
            self.name = name
        if email:
            self.email = email
        if password:
            self.set_password(password)
        if department:  # Update department if provided
            self.set_department(department)
        # Access level change is restricted for Admin

    def set_department(self, department: str):
        """Set the department for the admin."""
        self.department = department

    def verify_claim(self, claim_id: str) -> bool:
        """
        Verify a claim based on the claim ID.
        """
        # Implement the logic to verify the claim
        return True

    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a report for the admin with relevant details.
        """
        # Sample report generation (customize this as per your requirements)
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "access_level": self.access_level,
            "department": self.department,
            "status": "Active"  # Example additional field
        }



class AdminCLI:
    def __init__(self, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager
        self.admin = None
        self.current_user = None

    def create_admin_account(self):
        print("\n=== Create Admin Account ===")
        email = input("Enter admin email: ").strip()
        password = input("Enter admin password: ").strip()

        # Create the admin using the AuthenticationManager
        self.admin = Admin.create_admin(email, password, self.auth_manager)

        if self.admin:
            department = input("Enter department: ").strip()
            access_level = input("Enter access level: ").strip()

            # Directly set access level and department
            self.admin.access_level = access_level  # Set access level directly
            self.admin.department = department  # Set department directly
            print("Admin account created and configured successfully!")
        else:
            print("Failed to create admin account.")

    def login(self):
        print("\n=== Admin Login ===")
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()

        success, token = self.auth_manager.login(email, password)
        if success:
            self.current_user = email
            print("Login successful!")
        else:
            print(f"Login failed: {token}")

    def admin_menu(self):
        if self.admin is None:
            print("Admin account not created yet. Please create an admin account first.")
            return  # Exit the method early if admin is not created

        while True:
            print("\n=== Admin Menu ===")
            print("1. Verify Claim")
            print("2. Manage Policy")
            print("3. Generate Report")
            print("4. Audit User Actions")
            print("5. Logout")

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                claim_id = input("Enter claim ID: ").strip()
                if self.admin.verify_claim(claim_id):
                    print("Claim verified successfully!")
                else:
                    print("You do not have the privilege to verify claims.")
            elif choice == "2":
                policy_id = input("Enter policy ID: ").strip()
                if self.admin.manage_policy(policy_id):
                    print("Policy managed successfully!")
                else:
                    print("You do not have the privilege to manage policies.")
            elif choice == "3":
                report = self.admin.generate_report()
                print("\n=== Admin Report ===")
                for key, value in report.items():
                    print(f"{key}: {value}")
            elif choice == "4":
                user_id = input("Enter user ID: ").strip()
                actions = self.admin.audit_user_actions(user_id) if self.admin else []
                if actions:
                    print("\n=== User Actions ===")
                    for action in actions:
                        print(f"- {action}")
                else:
                    print("No actions found.")
            elif choice == "5":
                print("Logging out...")
                self.current_user = None
                break
            else:
                print("Invalid choice. Please try again.")

    def run(self):
        while True:
            print("\n=== Admin System ===")
            print("1. Create Admin Account")
            print("2. Login")
            print("3. Admin Menu")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                self.create_admin_account()
            elif choice == "2":
                self.login()
            elif choice == "3":
                if self.current_user:
                    self.admin_menu()
                else:
                    print("Please login first.")
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    auth_manager = AuthenticationManager()
    admin_cli = AdminCLI(auth_manager)
    admin_cli.run()
