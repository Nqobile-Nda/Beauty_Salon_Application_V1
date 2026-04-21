import json
import time


def load_catalog():
    try:
        with open("catalog.json", "r") as file:
            data = json.load(file)
            catalog = data.get("catalog", [])
    except (FileNotFoundError, json.JSONDecodeError):
        catalog = []
        with open("catalog.json", "w") as file:
            json.dump({"next_id": 1,"catalog": catalog}, file, indent=4)
    return catalog


def generate_item_id():
    with open("catalog.json", "r") as file:
        item_id = json.load(file).get("next_id", 1)
        next_id = item_id + 1
    return item_id, next_id


def add_item(new_item):
    with open("catalog.json", "r") as file:
        data =  json.load(file)

        next_id = data.get("next_id", 1)
        catalog  = data.get("catalog", [])
        
    catalog.append(new_item)

    with open("catalog.json", "w") as file:
        json.dump({"next_id": next_id + 1, "catalog": catalog}, file, indent=4)


def save_items(catalog):
    with open("catalog.json", "r") as file:
        next_id = json.load(file).get("next_id", 1)

    with open("catalog.json", "w") as file:
        json.dump({"next_id": next_id, "catalog": catalog}, file, indent=4)


def update_item(item_id, item_name, item_price, item_category, item_image, item_description, created_at, updated_at):
    catalog = load_catalog()

    for item in catalog:
        if item["item_id"] == item_id:
            item["name"] = item_name
            item["price"] = item_price
            item["category"] = item_category
            item["image"] = item_image
            item["description"] = item_description
            item["created_at"] = created_at
            item["updated_at"] = updated_at
            
    save_items(catalog)
    print("Saved")


def delete_item(item_id):
    catalog = load_catalog()
    for item in catalog:
        if item.get("item_id") == item_id:
            catalog.remove(item)
            save_items(catalog)
            print(f"{item} has been deleted.")


def filtered_catalog(category):
    catalog = load_catalog()
    items = [item for item in catalog if item.get("category") == category]
    return items


def load_user_booking_requests():
    try:
        with open("booking_requests.json", "r") as file:
            data = json.load(file)
            booking_requests = data.get("booking_requests", [])

    except (FileNotFoundError, json.JSONDecodeError):
        booking_requests = []
        with open("booking_requests.json", "w") as file:
            json.dump({"next_id": 1, "booking_requests": booking_requests}, file, indent=4)
    return booking_requests


def generate_booking_request_id():
    load_user_booking_requests()
    with open("booking_requests.json", "r") as file:
        data = json.load(file)
        request_id = data.get("next_id", 1)

        next_id = request_id + 1
    return request_id, next_id


def add_user_booking_requests(new_request):
    booking_requests = load_user_booking_requests()
    _, next_id = generate_booking_request_id()

    booking_requests.append(new_request)
    with open("booking_requests.json", "w") as file:
        json.dump({"next_id": next_id, "booking_requests": booking_requests}, file, indent=4)


def load_appointments():
    try:
        with open("appointments.json", "r") as file:
            appointments = json.load(file).get("appointments", [])
    except(FileNotFoundError, json.JSONDecodeError):
        appointments = []
        with open("appointments.json", "w") as file:
            json.dump({"next_id": 1,"appointments": appointments}, file, indent=4)
    return appointments


def generate_appointment_id():
    load_appointments()
    with open("appointments.json", "r") as file:
        appointment_id = json.load(file).get("next_id", 1)
        next_id = appointment_id + 1
        return appointment_id, next_id


def save_appointments(appointments):
    with open("appointments.json", "r") as file:
        next_id = json.load(file).get("next_id", 1)

    with open("appointments.json", "w") as file:
        json.dump({"next_id": next_id, "appointments": appointments}, file, indent=4)


def save_booking_requests(booking_requests):
    with open("booking_requests.json", "r") as file:
        next_id = json.load(file).get("next_id", 1)

    with open("booking_requests.json", "w") as file:
        json.dump({"next_id": next_id, "booking_requests": booking_requests}, file, indent=4)


def create_appointment(booking_request):
    appointments = load_appointments()
    appointment_id = booking_request.get("appointment_id")
    if appointment_id is None:
        appointment_id, next_id = generate_appointment_id()
        booking_request["appointment_id"] = appointment_id
    else:
        _, next_id = generate_appointment_id()

    booking_request.setdefault("status", "confirmed")
    appointments.append(booking_request)

    with open("appointments.json", "w") as file:
        json.dump({"next_id": next_id, "appointments": appointments}, file, indent=4)
    


def accept_appointment_status(request_id):
    booking_requests = load_user_booking_requests()

    item = next((item for item in booking_requests if item.get("request_id") == request_id), None)
    if item:
        item["status"] = "Confirmed"

    save_booking_requests(booking_requests)
    

def decline_appointment_status(request_id):
    booking_requests = load_user_booking_requests()

    item = next((item for item in booking_requests if item.get("request_id") == request_id), None)
    if item:
        item["status"] = "Declined"

    save_booking_requests(booking_requests)


def cancel_appointment_status(appointment_id):
    booking_requests = load_user_booking_requests()
    appointments = load_appointments()

    appointment = next((item for item in appointments if item.get("appointment_id") == appointment_id), None)
    if not appointment:
        return False

    request_id = appointment.get("request_id")
    if request_id is not None:
        booking_request = next((item for item in booking_requests if item.get("request_id") == request_id), None)
        if booking_request:
            booking_request["status"] = "Cancelled"
        save_booking_requests(booking_requests)

    updated_appointments = [item for item in appointments if item.get("appointment_id") != appointment_id]
    save_appointments(updated_appointments)
    return True


def complete_appointment_status(appointment_id):
    booking_requests = load_user_booking_requests()
    appointments = load_appointments()

    appointment = next((item for item in appointments if item.get("appointment_id") == appointment_id), None)
    if not appointment:
        return False

    request_id = appointment.get("request_id")
    if request_id is not None:
        booking_request = next((item for item in booking_requests if item.get("request_id") == request_id), None)
        if booking_request:
            booking_request["status"] = "Completed"
        save_booking_requests(booking_requests)

    updated_appointments = [item for item in appointments if item.get("appointment_id") != appointment_id]
    save_appointments(updated_appointments)
    return True
