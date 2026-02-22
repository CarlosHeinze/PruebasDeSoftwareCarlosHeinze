"""
This module implements a hotel system that allows Customers to
Create Reservations in a Hotel.
@author: Carlos Antonio Heinze Mortera
"""
from typing import Dict, Any, Optional


class Hotel(BaseClass):
    """Hotel class to manage hotel data and behaviors."""

    def get_filename(self) -> str:
        return "hotels.json"

    def create_hotel(self, hotel_id: str, name: str,
                     location: str, rooms: int) -> None:
        """
        Creates a new hotel entry and saves it to a JSON file.

        Parameters:
            hotel_id (str): ID for the Hotel to be created
            name (str): Name of the hotel to be created
            location (str): City where the hotel is located
            room (int): Number of rooms available in the hotel
        """
        data = self.load_data()
        if hotel_id in data:
            print(f"Error: Hotel ID '{hotel_id}' already exists.")
            return False
            
        data[hotel_id] = {"name": name, "location": location, "rooms": rooms}
        self.save_data(data)
        return True

    def delete_hotel(self, hotel_id: str) -> None:
        """
        Deletes a hotel based on the ID from the JSON file

        Returns:
            (bool): True if Hotel was in the JSON and could be
                    deleted. False if it was not found. 
        """
        data = self.load_data()
        if hotel_id in data:
            del data[hotel_id]
            self.save_data(data)
            return True
        return False

    def display_hotel(self, hotel_id: str) -> Dict[str, Any]:
        """Displays the information in consol and return it"""
        data = self.load_data()
        if hotel_id in data:
             hotel_information = data[hotel_id]
            print(f"Consulted Hotel: {hotel_information}")
            return hotel_information
        return False
       

    def modify_hotel(self, hotel_id: str, name: Optional[str] = None,
                     location: Optional[str] = None,
                     rooms: Optional[int] = None) -> None:
        """
        Modifies existing hotel attributes from the JSON file

        Returns:
            (bool): Return True if a modification was possible and 
                    False if not.
        """
        data = self.load_data()
        if hotel_id in data:
            if name is not None:
                data[hotel_id]["name"] = name
            if location is not None:
                data[hotel_id]["location"] = location
            if rooms is not None:
                data[hotel_id]["rooms"] = rooms
            self.save_data(data)
            return True
        return False

    def reserve_room(self, hotel_id: str) -> bool:
        """Decrements the available rooms if greater than zero."""
        data = self.load_data()
        if hotel_id in data and data[hotel_id]["rooms"] > 0:
            data[hotel_id]["rooms"] -= 1
            self.save_data(data)
            return True
        return False

    def cancel_reservation(self, hotel_id: str) -> bool:
        """Increments the available rooms for a given hotel."""
        data = self.load_data()
        if hotel_id in data:
            data[hotel_id]["rooms"] += 1
            self.save_data(data)
            return True
        return False


class Customer(BaseClass):
    """Customer class to manage customer records."""

    def get_filename(self) -> str:
        return "customers.json"

    def create_customer(self, customer_id: str, name: str, email: str) -> None:
        """
        Creates a new customer and saves it.

        Returns:
            (bool): True if the customer is created and Falase if it already 
                    exists
        """
        data = self.load_data()
        if customer_id in data:
            print(f"Error: Customer ID '{customer_id}' already exists.")
            return False
            
        data[customer_id] = {"name": name, "email": email}
        self.save_data(data)
        return True

    def delete_customer(self, customer_id: str) -> None:
        """
        Deletes a customer by ID.
        
        Returns:
            (bool): True if customer was in the JSON and could be
                    deleted. False if it was not found. 
        """
        data = self.load_data()
        if customer_id in data:
            del data[customer_id]
            self.save_data(data)
            return True
        return False

    def display_customer(self, customer_id: str) -> Dict[str, Any]:
        """Returns customer data as a dictionary."""
        data = self.load_data()
        if customer_id in data:
            customer_information = data[customer_id]
            print(f"Customer Requested: {customer_information}")
            return customer_information
        return False
        

    def modify_customer(self, customer_id: str, name: Optional[str] = None,
                        email: Optional[str] = None) -> None:
        """Modifies customer information and updates the file."""
        data = self.load_data()
        if customer_id in data:
            if name is not None:
                data[customer_id]["name"] = name
            if email is not None:
                data[customer_id]["email"] = email
            self.save_data(data)
            return True
        return False


class Reservation(BaseClass):
    """Reservation class linking customers and hotels."""

    def __init__(self, hotel_system: Hotel):
        """Initialize with a reference to a Hotel system to check rooms."""
        self.hotel_system = hotel_system

    def get_filename(self) -> str:
        return "reservations.json"

    def create_reservation(self, res_id: str, customer_id: str,
                           hotel_id: str) -> bool:
        """
        Creates a reservation if the hotel has available rooms.
        
        Returns:
            (bool): True if reservation successful.
        """
        if self.hotel_system.reserve_room(hotel_id):
            data = self.load_data()
            data[res_id] = {"customer_id": customer_id, "hotel_id": hotel_id}
            self.save_data(data)
            return True
        return False

    def display_reservation(self, res_id: str) -> Dict[str, Any]:
        """Returns reservation data as a dictionary."""
        data = self.load_data()
        if res_id in data:
            reservation_information = data[res_id]
            print(f'Reservation consulted: {reservation_information}')
            return reservation_information
        return False

    def cancel_reservation(self, res_id: str) -> bool:
        """
        Cancels a reservation and frees up a hotel room.
        
        Returns:
            (bool): True if reservation was in the JSON and could be
                    deleted. False if it was not found. 
        """
        data = self.load_data()
        if res_id in data:
            hotel_id = data[res_id]["hotel_id"]
            if self.hotel_system.cancel_reservation(hotel_id):
                del data[res_id]
                self.save_data(data)
                return True
        return False