"""
Unit tests for the hotel reservation system.
"""

import unittest
import os
from hotel_system import Hotel, Customer, Reservation


class TestHotel(Hotel):
    """Test Hotel Class to avoid overwriting production files"""
    def get_filename(self) -> str:
        return "test_hotels.json"


class TestCustomer(Customer):
    """Test Customer Class to avoid overwriting production files"""
    def get_filename(self) -> str:
        return "test_customers.json"


class TestReservation(Reservation):
    """Test Reservation Class to avoid overwriting production files"""
    def get_filename(self) -> str:
        return "test_reservations.json"


class TestHotelSystem(unittest.TestCase):
    """Test suite for the hotel reservation system."""

    def setUp(self):
        """Set up test environment with instantiated objects."""
        self.hotel = TestHotel()
        self.customer = TestCustomer()
        self.reservation = TestReservation(self.hotel)
        self._remove_files()

    def tearDown(self):
        """Clean up test files after each test."""
        self._remove_files()

    def _remove_files(self):
        """
        Removes the temporary JSON files after each test and 
        during Setup.
        """
        for filename in [self.hotel.get_filename(),
                         self.customer.get_filename(),
                         self.reservation.get_filename()]:
            if os.path.exists(filename):
                os.remove(filename)

    def test_hotel_operations(self):
        """Test hotel creation, validation, display, modification, deletion."""
        # Test display and modify on an ID that doesnt exist
        self.assertFalse(self.hotel.display_hotel("HO_1"))
        self.assertFalse(self.hotel.modify_hotel("HO_1", name="Fail"))

        # Test creating a Hotel successfully 
        self.assertTrue(self.hotel.create_hotel("HO_1", "HolidayInn", "QRO", 10))

        # Test creating a Hotel with a repeated ID
        self.assertFalse(self.hotel.create_hotel("HO_1", "HolidayInnDup", "QRO", 5))

        # Test getting data for the created hotel
        hotel_data = self.hotel.display_hotel("HO_1")
        self.assertNotEqual(hotel_data, False)
        self.assertEqual(hotel_data["name"], "HolidayInn")

        # Test successful modification
        self.assertTrue(self.hotel.modify_hotel("HO_1", name="FiestaInn", rooms=15))
        hotel_data = self.hotel.display_hotel("HO_1")
        self.assertEqual(hotel_data["name"], "FiestaInn")
        self.assertEqual(hotel_data["rooms"], 15)

        # Test successful deletion
        self.assertTrue(self.hotel.delete_hotel("HO_1"))
        self.assertFalse(self.hotel.display_hotel("HO_1"))
        
        # Test failed deletion (ID no longer exists)
        self.assertFalse(self.hotel.delete_hotel("HO_1"))

    def test_customer_operations(self):
        """Test customer creation, validation, display, modification, deletion."""
        # Test display and modify on a Customer ID that doesnt exist
        self.assertFalse(self.customer.display_customer("CT_1"))
        self.assertFalse(self.customer.modify_customer("CT_1", name="Fail"))

        # Test Successful creation of a customer
        self.assertTrue(
            self.customer.create_customer("CT_1", "Carlos", "cheinze@gmail.com")
        )

        # Test creating a customer with a repeated ID
        self.assertFalse(
            self.customer.create_customer("CT_1", "Daniel", "drincon@hotmail.com")
        )

        # Test the display of a valid customer ID
        cust_data = self.customer.display_customer("CT_1")
        self.assertNotEqual(cust_data, False)
        self.assertEqual(cust_data["name"], "Carlos")

        # Test successful modification
        self.assertTrue(self.customer.modify_customer("CT_1", name="Charlie"))
        cust_data = self.customer.display_customer("CT_1")
        self.assertEqual(cust_data["name"], "Charlie")

        # Test successful deletion
        self.assertTrue(self.customer.delete_customer("CT_1"))
        self.assertFalse(self.customer.display_customer("CT_1"))
        
        # Test failed deletion (ID does not exist)
        self.assertFalse(self.customer.delete_customer("CT_1"))

    def test_reservation_operations(self):
        """Test creating, displaying, and canceling reservations."""

        # Create the customers and hotels to create the reservation
        self.hotel.create_hotel("HO_2", "Continental", "CDMX", 1)
        self.customer.create_customer("CT_2", "Jorge", "JLopez@outlook.com")

        # Test display on non-existent ID
        self.assertFalse(self.reservation.display_reservation("Res_1"))

        # Test creating a successful reservation
        self.assertTrue(self.reservation.create_reservation("Res_1", "CT_2", "HO_2"))

        # Test that the Hotel rooms are 1 less than the creation
        self.assertEqual(self.hotel.display_hotel("HO_2")["rooms"], 0)

        # Test creating a reservation with an existing ID
        self.assertFalse(self.reservation.create_reservation("Res_1", "CT_2", "HO_2"))

        # Test creating a reservation in a Hotel with 0 rooms
        self.assertFalse(self.reservation.create_reservation("Res_2", "CT_2", "HO_2"))

        # Test the display method of reservation
        res_data = self.reservation.display_reservation("Res_1")
        self.assertNotEqual(res_data, False)
        self.assertEqual(res_data["customer_id"], "CT_2")

        # Cancel reservation successfully
        self.assertTrue(self.reservation.cancel_reservation("Res_1"))
        self.assertEqual(self.hotel.display_hotel("HO_2")["rooms"], 1)

        # Confirm it no longer displays
        self.assertFalse(self.reservation.display_reservation("Res_1"))

        # Attempt to cancel non-existent reservation
        self.assertFalse(self.reservation.cancel_reservation("Res_1"))
        self.assertFalse(self.reservation.cancel_reservation("Res_99"))

    def test_invalid_json_handling(self):
        """Test the system's ability to handle malformed JSON."""
        with open(self.hotel.get_filename(), "w", encoding="utf-8") as file:
            file.write("invalid json {")

        data = self.hotel.load_data()
        self.assertEqual(data, {})


if __name__ == "__main__":
    unittest.main()