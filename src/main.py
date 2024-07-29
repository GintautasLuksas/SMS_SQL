from worker import Worker

def main():
    worker = Worker()

    # Create the Worker table if it doesn't exist
    worker.create_table()

    # Menu for user interaction
    while True:
        print("\nWorker Table Menu:")
        print("1. Insert Data")
        print("2. View All Data")
        print("3. Update Data")
        print("4. Delete Data")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Insert Data
            worker_id = int(input("Enter WorkerID: "))
            name = input("Enter Name: ")
            phone_number = int(input("Enter Phone Number: "))
            email = input("Enter Email: ")
            country = input("Enter Country: ")
            hourly_rate = int(input("Enter Hourly Rate: "))
            amount_worked = int(input("Enter Amount Worked: "))
            worker.insert_data((worker_id, name, phone_number, email, country, hourly_rate, amount_worked))
            print("Data inserted successfully.")

        elif choice == '2':
            # View All Data
            data = worker.select_all()
            for row in data:
                print(row)

        elif choice == '3':
            # Update Data
            worker_id = int(input("Enter WorkerID to update: "))
            print("Enter new values (leave blank to keep current value):")
            name = input("New Name: ") or None
            phone_number = input("New Phone Number: ") or None
            email = input("New Email: ") or None
            country = input("New Country: ") or None
            hourly_rate = input("New Hourly Rate: ") or None
            amount_worked = input("New Amount Worked: ") or None

            new_values = {}
            if name is not None: new_values['Name'] = name
            if phone_number is not None: new_values['PhoneNumber'] = int(phone_number)
            if email is not None: new_values['Email'] = email
            if country is not None: new_values['Country'] = country
            if hourly_rate is not None: new_values['HourlyRate'] = int(hourly_rate)
            if amount_worked is not None: new_values['AmountWorked'] = int(amount_worked)

            worker.update_data(worker_id, new_values)
            print("Data updated successfully.")

        elif choice == '4':
            # Delete Data
            worker_id = int(input("Enter WorkerID to delete: "))
            worker.delete_data(worker_id)
            print("Data deleted successfully.")

        elif choice == '5':
            # Exit
            break

        else:
            print("Invalid choice. Please try again.")

    worker.close()

if __name__ == "__main__":
    main()
