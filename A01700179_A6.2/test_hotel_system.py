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

    def test_hotel_creation(self):
        """Test creating a Hotel successfully and with a repeated ID"""
        self.assertTrue(self.hotel.create_hotel("HO_1", "Homestay", "QRO", 10))

        # Test creating a Hotel with a repeated ID
        self.assertFalse(self.hotel.create_hotel("HO_1", "Dup", "QRO", 5))

    def test_hotel_display(self):
        """Test getting data for the created hotel"""
        self.hotel.create_hotel("HO_1", "Homestay", "QRO", 10)

        hotel_data = self.hotel.display_hotel("HO_1")
        self.assertNotEqual(hotel_data, False)
        self.assertEqual(hotel_data["name"], "Homestay")

        # Test negative case for display an ID that doesnt exist
        self.assertFalse(self.hotel.display_hotel("HO_98"))

    def test_hotel_modification(self):
        """Test Hotel Modification Method"""
        self.hotel.create_hotel("HO_1", "Homestay", "QRO", 10)

        self.assertTrue(
            self.hotel.modify_hotel("HO_1", name="FiestaInn", rooms=15)
        )
        hotel_data = self.hotel.display_hotel("HO_1")
        self.assertEqual(hotel_data["name"], "FiestaInn")
        self.assertEqual(hotel_data["rooms"], 15)

        # Test negative modification for a Hotel that does not exist
        self.assertFalse(
            self.hotel.modify_hotel("HO_99", name="One", rooms=15)
        )

    def test_hotel_deletion(self):
        """Test Hotel deletion"""
        self.hotel.create_hotel("HO_1", "Homestay", "QRO", 10)

        # Test successful deletion of a Hotel ID that exists
        self.assertTrue(self.hotel.delete_hotel("HO_1"))
        self.assertFalse(self.hotel.display_hotel("HO_1"))

        # Test failed deletion (ID no longer exists)
        self.assertFalse(self.hotel.delete_hotel("HO_1"))

    def test_customer_creation(self):
        """Test creation of a customer"""
        self.assertTrue(
            self.customer.create_customer("CT_1", "Carlos", "carlos@gmail.com")
        )

        # Test creating a customer with a repeated ID
        self.assertFalse(
            self.customer.create_customer("CT_1", "Daniel", "daniel@gmail.com")
        )

    def test_customer_display(self):
        """Test the display of a valid customer ID"""
        self.customer.create_customer("CT_1", "Carlos", "carlos@gmail.com")

        # Test display a customer ID that exists
        cust_data = self.customer.display_customer("CT_1")
        self.assertNotEqual(cust_data, False)
        self.assertEqual(cust_data["name"], "Carlos")

        # Test display a Customer ID that doesnt exist
        self.assertFalse(self.customer.display_customer("CT_56"))

    def test_customer_modification(self):
        """Test the Modification function of a customer"""
        self.customer.create_customer("CT_1", "Carlos", "carlos@gmail.com")

        # Test modify a Customer ID that exists
        self.assertTrue(self.customer.modify_customer("CT_1", name="Charlie"))
        cust_data = self.customer.display_customer("CT_1")
        self.assertEqual(cust_data["name"], "Charlie")

        # Test modify on a Customer ID that doesnt exist
        self.assertFalse(self.customer.modify_customer("CT_99", name="Fail"))

    def test_customer_deletion(self):
        """Test the deletion function of customer"""
        self.customer.create_customer("CT_1", "Carlos", "carlos@gmail.com")

        # Test successful deletion of customer ID that exists
        self.assertTrue(self.customer.delete_customer("CT_1"))
        self.assertFalse(self.customer.display_customer("CT_1"))

        # Test failed deletion (ID does not exist)
        self.assertFalse(self.customer.delete_customer("CT_1"))

    def test_reservation_creation(self):
        """Test the create function of the Reservation class"""

        self.hotel.create_hotel("HO_2", "Continental", "CDMX", 1)
        self.customer.create_customer("CT_2", "Jorge", "JLopez@outlook.com")

        # Test creating a successful reservation
        self.assertTrue(
            self.reservation.create_reservation("Res_1", "CT_2", "HO_2")
        )

        # Test that the Hotel rooms are 1 less than the creation
        self.assertEqual(self.hotel.display_hotel("HO_2")["rooms"], 0)

        # Test creating a reservation with an existing ID
        self.assertFalse(
            self.reservation.create_reservation("Res_1", "CT_2", "HO_2")
        )

        # Test creating a reservation in a Hotel with 0 rooms
        self.assertFalse(
            self.reservation.create_reservation("Res_2", "CT_2", "HO_2")
        )

    def test_reservation_display(self):
        """Test the Display finctionality of the Reservation class"""

        self.hotel.create_hotel("HO_2", "Continental", "CDMX", 1)
        self.customer.create_customer("CT_2", "Jorge", "JLopez@outlook.com")
        self.reservation.create_reservation("Res_1", "CT_2", "HO_2")

        # Test the display method of reservation
        res_data = self.reservation.display_reservation("Res_1")
        self.assertNotEqual(res_data, False)
        self.assertEqual(res_data["customer_id"], "CT_2")

        # Test display on non-existent ID
        self.assertFalse(self.reservation.display_reservation("Res_99"))

    def test_reservation_cancelation(self):
        """Test the cancelation function of the Reservation class"""

        self.hotel.create_hotel("HO_2", "Continental", "CDMX", 1)
        self.customer.create_customer("CT_2", "Jorge", "JLopez@outlook.com")
        self.reservation.create_reservation("Res_1", "CT_2", "HO_2")

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
