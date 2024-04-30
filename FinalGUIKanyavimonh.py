import tkinter as tk
import random
from tkinter import messagebox, simpledialog
from DataStructuresFinalKanyavimonh import LabQueue, LabTest, LabOrder


class LabManagementGUI(LabTest, LabOrder, LabQueue):
    def __init__(self, root):
        super().__init__(name="")
        self.root = root
        self.root.title("Lab GUI")
        self.root.geometry("700x900")  # Set the width to 600 pixels and height to 450 pixels

        self.CBC = LabTest("CBC")
        self.BMP = LabTest("BMP")
        self.TSH = LabTest("TSH")
        self.lab_queue = LabQueue()

        # Display the patient queue information
        self.display_patient_queue()

        # Display the stock queue information
        self.display_stock_queue()

        # Create GUI components
        self.label = tk.Label(root, text="Lab Management System", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)  # Adjust columnspan for wider label

        self.enqueue_button = tk.Button(root, text="Place Lab Order", command=self.enqueue_lab_order, width=20,
                                        height=3)
        self.enqueue_button.grid(row=1, column=0, padx=10, pady=10)

        self.process_button = tk.Button(root, text="Process Lab Order", command=self.process_lab_order, width=20,
                                        height=3)
        self.process_button.grid(row=1, column=1, padx=10, pady=10)

        self.generate_patient_button = tk.Button(root, text="Generate Patient", command=self.generate_patient, width=20,
                                                 height=3)
        self.generate_patient_button.grid(row=1, column=2, padx=10, pady=10)

    def view_stock(self):
        # Create a new window
        stock_window = tk.Toplevel(self.root)
        stock_window.title("Current Stock")

        # Label for the window
        label = tk.Label(stock_window, text="Current Stock")
        label.pack()

        # Function to update the stock information
        def update_stock():
            # Clear previous stock information
            for widget in stock_window.winfo_children():
                widget.destroy()

            # Iterate through each test in the LabTest instances
            for test in (self.CBC, self.BMP, self.TSH):
                test_label = tk.Label(stock_window, text=f"Test: {test.name}")
                test_label.pack()
                # Iterate through each item in the test's inventory
                for exp_date, amount in test.inventory:
                    inventory_label = tk.Label(stock_window, text=f"Amount: {amount}, Expiration Date: {exp_date}")
                    inventory_label.pack()

            # update stock window after 1 second
            stock_window.after(1000, update_stock)

        # Call update_stock initially to display current stock
        update_stock()

    def display_stock_queue(self):
        # Create a frame to contain the stock queue information
        stock_frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
        stock_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Label for the stock list
        label = tk.Label(stock_frame, text="Current Stock List", font=("Helvetica", 12))
        label.grid(row=0, column=0, columnspan=4, padx=10, pady=5)

        # Stock queue information
        stock_info = tk.Text(stock_frame, width=60, height=20)  # Increase height here
        stock_info.grid(row=4, column=0, columnspan=4, padx=10, pady=5)

        # Function to update the stock queue information
        def update_stock_info():
            # Clear previous stock queue information
            stock_info.delete('1.0', tk.END)

            # Insert updated stock queue information
            for test in (self.CBC, self.BMP, self.TSH):
                stock_info.insert(tk.END, f"Test: {test.name}\n")
                for exp_date, amount in test.inventory:
                    stock_info.insert(tk.END, f"  Amount: {amount}, Expiration Date: {exp_date}\n")
                stock_info.insert(tk.END, "\n")

            # Schedule the next update after 2 seconds
            stock_frame.after(500, update_stock_info)

        # Start the initial update of stock queue information
        update_stock_info()

        # Button to sort the supplies
        sort_button = tk.Button(stock_frame, text="Sort Supplies", command=self.sort_supplies)
        sort_button.grid(row=2, column=1, padx=10, pady=5)

        # Button to generate supplies
        generate_supplies_button = tk.Button(stock_frame, text="Order Supplies", command=self.generate_supplies)
        generate_supplies_button.grid(row=2, column=2, padx=10, pady=5)

    def display_patient_queue(self):
        # Create a frame to contain the patient queue information
        queue_frame = tk.Frame(self.root, bd=2, width=500, relief=tk.SUNKEN)
        queue_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Label for patient window
        label = tk.Label(queue_frame, text="Patient Queue", font=("Helvetica", 12))
        label.grid(row=0, column=0, columnspan=4, padx=10, pady=5)

        queue_info = tk.Text(queue_frame, width=80, height=10)
        queue_info.grid(row=1, column=0, columnspan=4, padx=10, pady=5)

        # Function to update the patient queue information
        def update_queue_info():
            # Clear previous patient queue information
            queue_info.delete('1.0', tk.END)

            # Insert updated patient queue information
            if self.lab_queue.is_empty():
                queue_info.insert(tk.END, "The patient queue is empty.")
            else:
                ranking = 1
                current_order = self.lab_queue.head
                while current_order is not None:
                    # Format patient ID to ensure it is 9 digits long with leading zeros
                    patient_id_formatted = str(current_order.patient_id).zfill(9)
                    queue_info.insert(tk.END,
                                      f"{ranking}: Patient ID: {patient_id_formatted}, Is STAT: {current_order.is_stat}, Tests Ordered: {current_order.print_ordered_tests()}\n")
                    current_order = current_order.next
                    ranking += 1

            # set update time to 500 miliseconds or .5 seconds.
            queue_frame.after(500, update_queue_info)

        # Start the initial update of patient queue information
        update_queue_info()
    def sort_supplies(self):
        # Sort the supplies for each test
        for test in (self.CBC, self.BMP, self.TSH):
            test.sort_inventory()

    def generate_patient(self):
        # Generate a random 9-digit patient ID
        patient_id = random.randint(100000000, 999999999)

        # Determine if the order is STAT
        is_stat = random.choice([True, False])

        # Create a lab order for the patient
        lab_order = LabOrder(patient_id, is_stat)

        # Add the specified tests to the lab order
        available_tests = [self.CBC, self.BMP, self.TSH]
        num_tests = random.randint(1, len(available_tests))  # Random number of tests to order
        ordered_tests = random.sample(available_tests, num_tests)  # Randomly select tests
        for test in ordered_tests:
            lab_order.add_test(test)

        # Add the lab order to the queue
        self.lab_queue.enqueue(lab_order)

    def generate_supplies(self):
        # Create a new window and make it stay on top
        supplies_window = tk.Toplevel(self.root)
        supplies_window.title("Generate Supplies")
        supplies_window.attributes('-topmost', True)

        # Label for the window
        label = tk.Label(supplies_window, text="Generate Supplies")
        label.pack()

        # Function to generate stock for a test
        def generate_stock(test):
            amount = random.randint(1, 10)  # Generate a random amount between 1 and 10
            exp_date = self.generate_random_exp_date()  # Generate a random expiration date
            test.add_inventory(amount=amount, exp_date=exp_date)

        # Iterate through each test in the LabTest instances
        for test in (self.CBC, self.BMP, self.TSH):
            test_label = tk.Label(supplies_window, text=f"Test: {test.name}")
            test_label.pack()

            # Button to generate stock for the test
            generate_button = tk.Button(supplies_window, text="Generate Stock",
                                        command=lambda t=test: generate_stock(t))
            generate_button.pack()

        # Keep the window in focus
        supplies_window.focus_force()

    def generate_random_exp_date(self):
        year = random.randint(2024, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Assuming all months have 28 days for simplicity
        return f"{year}-{month:02d}-{day:02d}"

    def enqueue_lab_order(self):
        patient_id = simpledialog.askinteger("Patient ID", "Enter Patient ID:")
        if patient_id is not None and 0 <= patient_id <= 999999999:
            is_stat = messagebox.askyesno("Is STAT", "Is this a STAT order?")
            lab_order = LabOrder(patient_id, is_stat)

            test_names = simpledialog.askstring("Test Names",
                                                "Enter Test Names separated by commas (e.g., CBC, BMP, TSH):")
            if test_names:
                test_names = [name.strip().upper() for name in test_names.split(",")]
                added_tests = set()  # Set to keep track of added tests
                for name in test_names:
                    if name == "CBC" and "CBC" not in added_tests:
                        lab_order.add_test(self.CBC)
                        added_tests.add("CBC")
                    elif name == "BMP" and "BMP" not in added_tests:
                        lab_order.add_test(self.BMP)
                        added_tests.add("BMP")
                    elif name == "TSH" and "TSH" not in added_tests:
                        lab_order.add_test(self.TSH)
                        added_tests.add("TSH")
                    else:
                        messagebox.showwarning("Invalid Test",
                                               f"Test '{name}' is not valid or already added to the order.")

                # Enqueues the order and sorts it as it goes into the queue
                self.lab_queue.enqueue(lab_order)
                messagebox.showinfo("Success", "Lab order added to the queue.")
            else:
                messagebox.showwarning("Invalid Test", "Please enter at least one test name.")
        else:
            messagebox.showwarning("Invalid Patient ID", "Please enter a valid patient ID between 0 and 999999999.")

    def process_lab_order(self):
        if self.lab_queue.is_empty():
            messagebox.showinfo("Process Lab Order", "There are no orders to process.")
        else:
            processed_order = self.lab_queue.head
            order_processed = self.lab_queue.process_lab_order()  # Process the first order in the queue
            if order_processed:
                pass
            else:
                messagebox.showwarning("Insufficient Stock",
                                       "Not enough stock available to process the tests. Please order stock.")

    def view_lab_queue(self):
        # Create a new window
        queue_window = tk.Toplevel(self.root)
        queue_window.title("Lab Queue")

        queue_info_label = [None]  # List to store the label window widget

        def update_queue():
            if queue_info_label[0]:
                queue_info_label[0].destroy()
            if self.lab_queue.is_empty():
                # Display a message if the queue is empty
                queue_info_label[0] = tk.Label(queue_window, text="The lab queue is empty.")
                queue_info_label[0].pack()
            else:
                # Display the lab queue with ranking numbers
                queue_info = ""
                ranking = 1
                current_order = self.lab_queue.head
                while current_order is not None:
                    # Format patient ID to ensure it is 9 digits long with leading zeros
                    patient_id_formatted = str(current_order.patient_id).zfill(9)
                    queue_info += f"{ranking}: Patient ID: {patient_id_formatted}, Is STAT: {current_order.is_stat}, Tests Ordered: {current_order.print_ordered_tests()}\n"
                    current_order = current_order.next
                    ranking += 1
                queue_info_label[0] = tk.Label(queue_window, text=queue_info)
                queue_info_label[0].pack()
            # Schedule the next update after 5 seconds
            queue_window.after(2000, update_queue)

        # Start the initial update
        update_queue()


if __name__ == "__main__":
    root = tk.Tk()
    app = LabManagementGUI(root)
    root.mainloop()
