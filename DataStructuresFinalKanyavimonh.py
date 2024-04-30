class LabTest:
    def __init__(self, name):
        self.name = name
        self.inventory = []

    def add_inventory(self, amount, exp_date):
        item_stock = (exp_date, amount)
        self.inventory.append(item_stock)
        print('item added')

    def view_stock(self):
        if len(self.inventory) > 0:
            print(f'{self.name} inventory in house\n{self.inventory}')
        else:
            print('No supplies in house, order more.')

    def sort_inventory(self):
        sorted_inventory = []
        for exp_date, amount in self.inventory:
            index = self.binary_search_insert(sorted_inventory, exp_date)
            sorted_inventory.insert(index, (exp_date, amount))
        print('inventory sorted')
        self.inventory = sorted_inventory

    def binary_search_insert(self, arr, key):
        low, high = 0, len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid][0] == key:
                return mid
            elif arr[mid][0] < key:
                low = mid + 1
            else:
                high = mid - 1
        return low

    def __str__(self):
        return self.name


class LabOrder:
    def __init__(self, patient_id, is_stat=False):
        print('Patient created')
        self.patient_id = patient_id
        self.ordered_tests = []
        self.is_stat = is_stat
        self.next = None

    def add_test(self, test):
        self.ordered_tests.append(test)
        print(f'{test} added')

    def print_ordered_tests(self):
        test_list = []
        if self.ordered_tests:
            for test in self.ordered_tests:
                test_list.append(test.name)
            return test_list
        else:
            return "No tests ordered for this patient yet."


class LabQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, lab_order):
        if lab_order.is_stat:
            if self.is_empty():
                self.head = lab_order
                self.tail = lab_order
            else:
                lab_order.next = self.head
                self.head = lab_order
        else:
            if self.is_empty():
                self.head = lab_order
                self.tail = lab_order
            else:
                self.tail.next = lab_order
                self.tail = lab_order

    def view_queue(self):
        if self.is_empty():
            print("The lab queue is empty.")
        else:
            print("Lab Queue:")
            current_order = self.head
            while current_order is not None:
                print(
                    f"Patient ID: {current_order.patient_id}, Is STAT: {current_order.is_stat}, Tests Ordered: {current_order.print_ordered_tests()}")
                current_order = current_order.next

    def process_lab_order(self):
        if self.is_empty():
            print('There are no orders to process.')
            return False

        processed_order = self.head
        self.head = self.head.next

        if self.head is None:
            self.tail = None

        if processed_order.ordered_tests:
            print(f"Processing patient {processed_order.patient_id}:")
            order_processed = True  # Flag to indicate if the order was processed successfully

            # Check if all tests have enough stock
            for test_info in processed_order.ordered_tests:
                test_name = test_info.name
                if not test_info.inventory:
                    print(f"No stock available for {test_name}.")
                    order_processed = False  # Set flag to False if stock is not available for any test
                else:
                    exp_date, stock = test_info.inventory[0]
                    amount_needed = 1  # Example amount needed
                    if stock < amount_needed:
                        print(f"Not enough stock of {test_name} to process.")
                        order_processed = False  # Set flag to False if stock is not enough for any test

            if order_processed:
                # If all tests have enough stock, process the order
                for test_info in processed_order.ordered_tests:
                    test_name = test_info.name
                    exp_date, stock = test_info.inventory[0]
                    stock -= amount_needed
                    print(f"{amount_needed} units of {test_name} processed. Remaining stock: {stock}")
                    test_info.inventory[0] = (exp_date, stock)  # Update the inventory tuple
                    if stock == 0:
                        test_info.inventory.pop(0)
                        print(
                            f"Current lot of {test_name} has been exhausted. Removing from inventory and updating lot list.")
                print("Lab order processed successfully.")
            else:
                print("Lab order not processed due to insufficient stock. Patient remains in the queue.")
                self.head = processed_order
                return False
        else:
            print("No tests ordered for this patient yet.")
            return False

        return True

if __name__ == '__main__':
    CBC = LabTest('CBC')
    CBC.add_inventory(amount=1, exp_date="2024-05-20")
    CBC.sort_inventory()
    BMP = LabTest('BMP')
    BMP.add_inventory(amount=2, exp_date="2024-01-01")
    BMP.add_inventory(amount=4, exp_date="2024-11-15")
    BMP.add_inventory(amount=1, exp_date="2024-08-20")
    BMP.sort_inventory()

    patient = LabOrder(123456)
    patient2 = LabOrder(654321, True)
    patient.add_test(CBC)
    patient.add_test(BMP)
    patient2.add_test(CBC)
    BMP.view_stock()
    CBC.view_stock()
    print('------------------------------------------')
    LabQ = LabQueue()
    LabQ.enqueue(patient)
    LabQ.enqueue(patient2)
    LabQ.view_queue()
    LabQ.process_lab_order()
    LabQ.view_queue()
    LabQ.process_lab_order()
    LabQ.process_lab_order()
    print('------------------------------------------')
    CBC.view_stock()
    BMP.view_stock()