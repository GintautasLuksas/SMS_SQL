from src.tables.worker_table import WorkerTable

def display_menu():
    """Display the menu options."""
    print("\nWorker Table Management")
    print("1. Add a new worker")
    print("2. Edit an existing worker")
    print("3. Delete a worker")
    print("4. View all workers")
    print("5. Exit")

def add_worker(worker_table):
    """Add a new worker to the table."""
    try:
        name = input("Enter worker's name: ")
        phone_number = int(input("Enter worker's phone number: "))
        email = input("Enter worker's email: ")
        country = input("Enter worker's country: ")
        hourly_rate = int(input("Enter worker's hourly rate: "))
        amount_worked = int(input("Enter amount worked: "))

        worker_table.insert_data((name, phone_number, email, country, hourly_rate, amount_worked))
        print("Worker added successfully!")
    except ValueError as e:
        print(f"Invalid input: {e}")

def edit_worker(worker_table):
    """Edit an existing worker's information."""
    try:
        worker_id = int(input("Enter the worker ID to edit: "))
        name = input("Enter new name (leave empty to keep current): ")
        phone_number = input("Enter new phone number (leave empty to keep current): ")
        email = input("Enter new email (leave empty to keep current): ")
        country = input("Enter new country (leave empty to keep current): ")
        hourly_rate = input("Enter new hourly rate (leave empty to keep current): ")
        amount_worked = input("Enter new amount worked (leave empty to keep current): ")

        # Collect only fields that are not empty
        new_values = {}
        if name:
            new_values['Name'] = name
        if phone_number:
            new_values['PhoneNumber'] = int(phone_number)
        if email:
            new_values['Email'] = email
        if country:
            new_values['Country'] = country
        if hourly_rate:
            new_values['HourlyRate'] = int(hourly_rate)
        if amount_worked:
            new_values['AmountWorked'] = int(amount_worked)

        if new_values:
            worker_table.update_data(worker_id, new_values)
            print("Worker updated successfully!")
        else:
            print("No changes were made.")
    except ValueError as e:
        print(f"Invalid input: {e}")

def delete_worker(worker_table):
    """Delete a worker from the table."""
    try:
        worker_id = int(input("Enter the worker ID to delete: "))
        worker_table.delete_data(worker_id)
        print("Worker deleted successfully!")
    except ValueError as e:
        print(f"Invalid input: {e}")

def view_workers(worker_table):
    """View all workers in the table."""
    workers = worker_table.select_all()
    if workers:
        print("\nWorkers in the table:")
        for worker in workers:
            print(worker)
    else:
        print("No workers found.")

def main():
    worker_table = WorkerTable()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_worker(worker_table)
        elif choice == '2':
            edit_worker(worker_table)
        elif choice == '3':
            delete_worker(worker_table)
        elif choice == '4':
            view_workers(worker_table)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please select between 1 and 5.")

if __name__ == "__main__":
    main()
