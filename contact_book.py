# Import required modules
import json  # For JSON file operations
import os  # For file existence check
from datetime import datetime  # For date/time tracking

# Main Contact Book class
class ContactBook:
    # Initialize with filename and load existing contacts
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = self.load_contacts()
    
    def load_contacts(self):
        """Load contacts from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error reading contacts file. Starting with empty contact list.")
                return {}
        return {}
    
    def save_contacts(self):
        """Save contacts to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.contacts, f, indent=4)
        print("Contacts saved successfully!")
    
    def add_contact(self, name, phone_number, email="", address=""):
        """Add a new contact"""
        # Check if contact already exists (case-insensitive)
        if name.lower() in [c.lower() for c in self.contacts]:
            print(f"Contact '{name}' already exists!")
            return False
        
        # Validate phone number before adding
        if not self.validate_phone(phone_number):
            print("Invalid phone number format!")
            return False
        
        # Store contact with all details and timestamp
        self.contacts[name] = {
            "phone": phone_number,
            "email": email,
            "address": address,
            "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_contacts()  # Save to file immediately
        print(f"Contact '{name}' added successfully!")
        return True
    
    def edit_contact(self, name, phone_number=None, email=None, address=None):
        """Edit an existing contact"""
        # Find contact case-insensitively
        contact_key = None
        for key in self.contacts:
            if key.lower() == name.lower():
                contact_key = key
                break
        
        if contact_key is None:
            print(f"Contact '{name}' not found!")
            return False
        
        if phone_number:
            if not self.validate_phone(phone_number):
                print("Invalid phone number format!")
                return False
            self.contacts[contact_key]["phone"] = phone_number
        
        if email:
            self.contacts[contact_key]["email"] = email
        
        if address:
            self.contacts[contact_key]["address"] = address
        
        self.save_contacts()
        print(f"Contact '{contact_key}' updated successfully!")
        return True
    
    def search_contact(self, query):
        """Search for contacts by name, phone, or email"""
        results = []
        query_lower = query.lower()
        
        # Search through all contacts
        for name, details in self.contacts.items():
            # Match by name (case-insensitive), phone (exact), or email (case-insensitive)
            if (query_lower in name.lower() or 
                query in details.get("phone", "") or
                query_lower in details.get("email", "").lower()):
                results.append((name, details))
        
        return results
    
    def delete_contact(self, name):
        """Delete a contact"""
        contact_key = None
        for key in self.contacts:
            if key.lower() == name.lower():
                contact_key = key
                break
        
        if contact_key is None:
            print(f"Contact '{name}' not found!")
            return False
        
        del self.contacts[contact_key]
        self.save_contacts()
        print(f"Contact '{contact_key}' deleted successfully!")
        return True
    
    def display_contact(self, name):
        """Display details of a specific contact"""
        contact_key = None
        for key in self.contacts:
            if key.lower() == name.lower():
                contact_key = key
                break
        
        if contact_key is None:
            print(f"Contact '{name}' not found!")
            return False
        
        details = self.contacts[contact_key]
        print(f"\n{'='*50}")
        print(f"Name: {contact_key}")
        print(f"Phone: {details.get('phone', 'N/A')}")
        print(f"Email: {details.get('email', 'N/A')}")
        print(f"Address: {details.get('address', 'N/A')}")
        print(f"Date Added: {details.get('date_added', 'N/A')}")
        print(f"{'='*50}\n")
        return True
    
    def list_all_contacts(self):
        """Display all contacts"""
        if not self.contacts:
            print("No contacts found!")
            return
        
        print(f"\n{'='*70}")
        print(f"{'Name':<20} {'Phone':<15} {'Email':<25}")
        print(f"{'='*70}")
        
        for name, details in self.contacts.items():
            phone = details.get("phone", "N/A")
            email = details.get("email", "N/A")
            print(f"{name:<20} {phone:<15} {email:<25}")
        
        print(f"{'='*70}\n")
    
    @staticmethod
    def validate_phone(phone_number):
        """Validate phone number - must have at least 10 digits"""
        # Remove separators (-, spaces, parentheses)
        clean_phone = phone_number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        # Count digits and ensure minimum of 10
        digits = sum(1 for c in clean_phone if c.isdigit())
        return digits >= 10


# Display menu options
def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("        CONTACT BOOK APPLICATION")
    print("="*50)
    print("1. Add a new contact")
    print("2. Search for a contact")
    print("3. Edit a contact")
    print("4. Delete a contact")
    print("5. Display a specific contact")
    print("6. List all contacts")
    print("7. Exit")
    print("="*50)


# Main application function
def main():
    """Main application loop - handles user interactions"""
    book = ContactBook()  # Initialize contact book
    
    # Continuous loop for user menu
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()  # Get user input
        
        # Option 1: Add new contact
        if choice == "1":
            name = input("Enter contact name: ").strip()
            phone = input("Enter phone number: ").strip()
            email = input("Enter email (optional): ").strip()
            address = input("Enter address (optional): ").strip()
            book.add_contact(name, phone, email, address)
        
        # Option 2: Search for contact
        elif choice == "2":
            query = input("Enter name, phone number, or email to search: ").strip()
            results = book.search_contact(query)
            
            if results:
                print(f"\n{'='*70}")
                print(f"Found {len(results)} result(s):")
                print(f"{'='*70}")
                for name, details in results:
                    print(f"\nName: {name}")
                    print(f"Phone: {details.get('phone', 'N/A')}")
                    print(f"Email: {details.get('email', 'N/A')}")
                    print(f"Address: {details.get('address', 'N/A')}")
                print(f"{'='*70}\n")
            else:
                print(f"No contacts found matching '{query}'!")
        
        # Option 3: Edit existing contact
        elif choice == "3":
            name = input("Enter contact name to edit: ").strip()
            print("Leave fields empty to skip editing")
            phone = input("Enter new phone number (optional): ").strip()
            email = input("Enter new email (optional): ").strip()
            address = input("Enter new address (optional): ").strip()
            book.edit_contact(name, phone or None, email or None, address or None)
        
        # Option 4: Delete contact
        elif choice == "4":
            name = input("Enter contact name to delete: ").strip()
            confirm = input(f"Are you sure you want to delete '{name}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                book.delete_contact(name)
            else:
                print("Deletion cancelled.")
        
        # Option 5: Display single contact details
        elif choice == "5":
            name = input("Enter contact name to display: ").strip()
            book.display_contact(name)
        
        # Option 6: List all contacts
        elif choice == "6":
            book.list_all_contacts()
        
        # Option 7: Exit application
        elif choice == "7":
            print("Thank you for using Contact Book! Goodbye!")
            break
        
        # Invalid option
        else:
            print("Invalid choice! Please try again.")


# Run application if executed directly
if __name__ == "__main__":
    main()
