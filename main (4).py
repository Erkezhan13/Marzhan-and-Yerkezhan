from datetime import datetime

# Base class for all vehicle types using polymorphism
class Vehicle:
    def __init__(self, license_plate, vehicle_type):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

# Subclass for cars
class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, vehicle_type=1)

# Subclass for trucks
class Truck(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, vehicle_type=2)

# Subclass for motorcycles
class Motorcycle(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, vehicle_type=0.5)

# Class for parking spots
class ParkingSpot:
    def __init__(self, spot_id, spot_size, is_occupied=False):
        self.spot_id = spot_id
        self.spot_size = spot_size
        self.is_occupied = is_occupied

    # Method to occupy a parking spot
    def occupy_spot(self):
        self.is_occupied = True

    # Method to free a parking spot
    def free_spot(self):
        self.is_occupied = False

# Class to manage the entire parking lot
class ParkingLot:
    def __init__(self):
        self.parking_spots = {}
        self.vehicle_spot_map = {}
        self.parked_time = {}
        self.daily_earnings = 0

    # Method to add parking spots to the lot
    def add_spot(self, spot_id, spot_size):
        self.parking_spots[spot_id] = ParkingSpot(spot_id, spot_size)

    # Method to park a vehicle
    def park_vehicle(self, vehicle):
        for spot_id, spot in self.parking_spots.items():
            if not spot.is_occupied and spot.spot_size >= vehicle.vehicle_type:
                spot.occupy_spot()
                self.vehicle_spot_map[vehicle.license_plate] = spot_id
                self.parked_time[vehicle.license_plate] = datetime.now()
                print(f"Vehicle {vehicle.license_plate} parked at spot {spot_id}")
                return True
        print("No available spot for vehicle.")
        return False

    # Method to release a parked vehicle and calculate fees
    def release_vehicle(self, vehicle):
        if vehicle.license_plate in self.vehicle_spot_map:
            spot_id = self.vehicle_spot_map.pop(vehicle.license_plate)
            duration = datetime.now() - self.parked_time.pop(vehicle.license_plate)
            hours = duration.total_seconds() / 3600
            rate = 2.5  # Base rate per hour
            if vehicle.vehicle_type == 2:  # Different rate for trucks
                rate *= 2
            fee = hours * rate
            self.daily_earnings += fee
            self.parking_spots[spot_id].free_spot()
            print(f"Vehicle {vehicle.license_plate} left spot {spot_id}. Total fee: ${fee:.2f}")
            return True
        print("Vehicle not found.")
        return False

    # Method to display the current status of parking spots
    def display_lot_status(self):
        for spot_id, spot in self.parking_spots.items():
            status = "Occupied" if spot.is_occupied else "Free"
            print(f"Spot {spot_id} is {status}")

    # Method to report daily earnings from the parking fees
    def report_daily_earnings(self):
        print(f"Total earnings today: ${self.daily_earnings:.2f}")

# CLI to interact with the parking lot system
def cli():
    lot = ParkingLot()
    lot.add_spot("1A", 1)  # Smaller spot for cars
    lot.add_spot("1B", 2)  # Larger spot for trucks
    lot.add_spot("MC1", 0.5)  # Spot for motorcycles

    while True:
        print("\n1. Park Vehicle\n2. Release Vehicle\n3. Lot Status\n4. Daily Earnings\n5. Exit")
        try:
            choice = input("Choose an action: ")
            if choice == '1':
                license_plate = input("Enter license plate: ")
                vehicle_type = input("Enter vehicle type (1=Car, 2=Truck, 0.5=Motorcycle): ")
                if vehicle_type == '1':
                    vehicle = Car(license_plate)
                elif vehicle_type == '2':
                    vehicle = Truck(license_plate)
                elif vehicle_type == '0.5':
                    vehicle = Motorcycle(license_plate)
                else:
                    raise ValueError("Invalid vehicle type provided.")
                lot.park_vehicle(vehicle)
            elif choice == '2':
                license_plate = input("Enter license plate to release: ")
                vehicle = Vehicle(license_plate, 1)  # Vehicle type doesn't affect release
                lot.release_vehicle(vehicle)
            elif choice == '3':
                lot.display_lot_status()
            elif choice == '4':
                lot.report_daily_earnings()
            elif choice == '5':
                break
            else:
                print("Invalid choice.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    cli()
