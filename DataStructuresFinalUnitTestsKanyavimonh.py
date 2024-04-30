import unittest
from DataStructuresFinalKanyavimonh import LabTest, LabOrder, LabQueue

class TestLabManagement(unittest.TestCase):
    def setUp(self):
        # Create sample lab tests
        self.CBC = LabTest("CBC")
        self.BMP = LabTest("BMP")
        self.TSH = LabTest("TSH")

    def test_lab_test_add_inventory(self):
        # Test adding inventory to a lab test
        self.CBC.add_inventory(10, "2024-04-20")
        self.assertEqual(len(self.CBC.inventory), 1)  # Check if inventory is added successfully

    def test_lab_test_sort_inventory(self):
        # Test sorting inventory of a lab test
        self.CBC.add_inventory(5, "2024-04-20")
        self.CBC.add_inventory(10, "2024-04-15")
        self.CBC.sort_inventory()
        self.assertEqual(self.CBC.inventory[0][1], 10)  # Check if inventory is sorted correctly

    def test_lab_order_add_test(self):
        # Test adding tests to a lab order
        order = LabOrder(123456789)
        order.add_test(self.CBC)
        order.add_test(self.BMP)
        self.assertEqual(len(order.ordered_tests), 2)  # Check if tests are added successfully

    def test_lab_queue_enqueue(self):
        # Test enqueuing lab orders into a lab queue
        lab_queue = LabQueue()
        order1 = LabOrder(123456789)
        order2 = LabOrder(987654321)
        lab_queue.enqueue(order1)
        lab_queue.enqueue(order2)
        self.assertEqual(lab_queue.head, order1)  # Check if orders are enqueued successfully

    def test_lab_queue_process_lab_order(self):
        # Test processing lab orders in a lab queue
        lab_queue = LabQueue()
        order1 = LabOrder(123456789)
        order1.add_test(self.CBC)
        order1.add_test(self.BMP)
        lab_queue.enqueue(order1)
        lab_queue.process_lab_order()
        self.assertIsNotNone(lab_queue.head)  # Lab order should still be present due to no supplies

    def test_process_lab_order_not_enough_stock(self):
        """
        Test checks scenario of partial stock available for test,
        queue should not move due to all tests not being completed.
        """
        cbc = LabTest("CBC")
        bmp = LabTest("BMP")

        # Set initial inventory for CBC and BMP
        cbc.add_inventory(amount=0, exp_date="2024-04-15")  # No stock for CBC
        bmp.add_inventory(amount=10, exp_date="2024-04-15")  # Sufficient stock for BMP

        # Create lab queue
        lab_queue = LabQueue()

        # Create lab order with CBC and BMP tests
        lab_order = LabOrder(patient_id=123456789, is_stat=False)
        lab_order.add_test(cbc)
        lab_order.add_test(bmp)

        # Enqueue lab order
        lab_queue.enqueue(lab_order)

        # Process lab order
        result = lab_queue.process_lab_order()

        # Ensure that the result is False (order not processed due to insufficient stock)
        self.assertFalse(result)

    def test_process_lab_order_sufficient_stock(self):
        # Create lab tests
        cbc = LabTest("CBC")
        bmp = LabTest("BMP")

        # Set initial inventory for CBC and BMP
        cbc.add_inventory(amount=10, exp_date="2024-04-15")  # Sufficient stock for CBC
        bmp.add_inventory(amount=10, exp_date="2024-04-15")  # Sufficient stock for BMP

        # Create lab queue
        lab_queue = LabQueue()

        # Create lab order with CBC and BMP tests
        lab_order = LabOrder(patient_id=123456789, is_stat=False)
        lab_order.add_test(cbc)
        lab_order.add_test(bmp)

        # Enqueue lab order
        lab_queue.enqueue(lab_order)

        # Process lab order
        result = lab_queue.process_lab_order()

        # Ensure that the result is True (order processed successfully)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()