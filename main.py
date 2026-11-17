
import json
import os

class MinHeap:
    def __init__(self):
        self.heap = []

    def compare(self, a, b):
        return (a["priority"], a["arrival"]) < (b["priority"], b["arrival"])

    def insert(self, patient):
        self.heap.append(patient)
        i = len(self.heap) - 1

        while i > 0:
            parent = (i - 1) // 2
            if self.compare(self.heap[i], self.heap[parent]):
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def remove(self):
        if not self.heap:
            return None

        patient = self.heap[0]
        last = self.heap.pop()

        if self.heap:
            self.heap[0] = last
            self.heapify(0)

        return patient

    def heapify(self, i):
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < len(self.heap) and self.compare(self.heap[left], self.heap[smallest]):
            smallest = left

        if right < len(self.heap) and self.compare(self.heap[right], self.heap[smallest]):
            smallest = right

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.heapify(smallest)

    def display(self):
        return sorted(self.heap, key=lambda p: (p["priority"], p["arrival"]))


waiting = MinHeap()
history = []
arrival_counter = 0

def save_data():
    data = {
        "waiting": waiting.heap,
        "history": history,
        "arrival_counter": arrival_counter
    }

    with open("patients.json", "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    global history, arrival_counter

    if os.path.exists("patients.json"):
        try:
            with open("patients.json", "r") as file:
                data = json.load(file)

            history = data.get("history", [])
            arrival_counter = data.get("arrival_counter", 0)

            for patient in data.get("waiting", []):
                waiting.insert(patient)

        except (json.JSONDecodeError, OSError):
            print("Could not load saved records.")

def register_patient():
    global arrival_counter

    print("\n--- PATIENT REGISTRATION ---")

    pid = input("Enter Patient ID: ").strip()

    if not pid:
        print("Patient ID cannot be empty.")
        return

    if any(p["id"] == pid for p in waiting.heap + history):
        print("Patient ID already exists.")
        return

    name = input("Enter Patient Name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    try:
        age = int(input("Enter Age: "))
        if age <= 0 or age > 120:
            print("Enter a valid age.")
            return
    except ValueError:
        print("Invalid age.")
        return

    condition = input("Enter Medical Condition: ").strip()

    if not condition:
        print("Condition cannot be empty.")
        return

    print("\nEmergency Level:")
    print("1. Critical")
    print("2. High")
    print("3. Moderate")
    print("4. Low")

    try:
        priority = int(input("Enter Priority: "))
        if priority not in [1, 2, 3, 4]:
            print("Invalid priority.")
            return
    except ValueError:
        print("Invalid input.")
        return

    arrival_counter += 1

    patient = {
        "id": pid,
        "name": name,
        "age": age,
        "condition": condition,
        "priority": priority,
        "arrival": arrival_counter
    }

    waiting.insert(patient)
    save_data()

    print("\nPatient registered successfully!")



def display_queue():
    if not waiting.heap:
        print("\nNo patients are waiting.")
        return

    patients = sorted(waiting.heap, key=lambda p: (p["priority"], p["arrival"]))

    print("\n========== WAITING PATIENTS ==========")
    print(f"{'ID':<8}{'Name':<15}{'Age':<8}{'Priority':<12}{'Condition'}")
    print("-" * 65)

    for p in patients:
        print(f"{p['id']:<8}{p['name']:<15}{p['age']:<8}{p['priority']:<12}{p['condition']}")

    print("======================================")



def edit_priority():
    if not waiting.heap:
        print("\nNo patients are waiting.")
        return

    patient_id = input("\nEnter Patient ID: ")

    patient = None

    for p in waiting.heap:
        if str(p["id"]) == patient_id:
            patient = p
            break

    if patient is None:
        print("\nPatient not found in waiting queue.")
        return

    print("\nPatient:", patient["name"])
    print("Current Priority:", patient["priority"])

    while True:
        try:
            new_priority = int(input("Enter new priority (1-4): "))
            if new_priority in [1, 2, 3, 4]:
                break
            print("Invalid priority! Enter between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")

    patient["priority"] = new_priority

    patients = waiting.heap[:]
    waiting.heap.clear()

    for p in patients:
        waiting.insert(p)

    save_data()

    print("\nPatient priority updated successfully!")



def treat_patient():
    print("\n--- PATIENT TREATMENT ---")

    patient = waiting.remove()

    if patient is None:
        print("No patients waiting.")
        return

    levels = {1: "CRITICAL", 2: "HIGH", 3: "MODERATE", 4: "LOW"}

    print("\nNext Patient:")
    print("Patient ID:", patient["id"])
    print("Name:", patient["name"])
    print("Condition:", patient["condition"])
    print("Priority:", levels[patient["priority"]])

    confirm = input("\nConfirm treatment? (Y/N): ").strip().upper()

    if confirm == "Y":
        patient["status"] = "Treated"
        history.append(patient)
        print("Patient treated successfully!")
    else:
        waiting.insert(patient)
        print("Treatment cancelled. Patient returned to queue.")

    save_data()

def search_patient():
    pid = input("\nEnter Patient ID to search: ").strip()

    for patient in waiting.heap + history:
        if patient["id"] == pid:
            print("\nPatient Found!")
            print("ID:", patient["id"])
            print("Name:", patient["name"])
            print("Age:", patient["age"])
            print("Condition:", patient["condition"])
            print("Status:", patient.get("status", "Waiting"))
            return

    print("Patient not found.")

def patient_history():
    print("\n--- TREATED PATIENT HISTORY ---")

    if not history:
        print("No treated patients yet.")
        return

    for p in history:
        print("ID:", p["id"], "| Name:", p["name"],
              "| Condition:", p["condition"], "| Status:", p["status"])

def statistics():
    print("\n--- HOSPITAL STATISTICS ---")
    print("Total Registered:", len(waiting.heap) + len(history))
    print("Currently Waiting:", len(waiting.heap))
    print("Patients Treated:", len(history))
    print("Critical Patients:", sum(1 for p in waiting.heap if p["priority"] == 1))

def main():
    load_data()

    while True:
        print("\n" + "=" * 45)
        print("   HOSPITAL EMERGENCY QUEUE MANAGEMENT")
        print("=" * 45)
        print("1. Register New Patient")
        print("2. Display Waiting Queue")
        print("3. Treat Next Patient")
        print("4. Search Patient")
        print("5. View Patient History")
        print("6. Hospital Statistics")
        print("7. Edit Patient Priority")
        print("8. Exit")
        print("=" * 45)

        choice = input("Enter your choice: ")

        if choice == "1":
            register_patient()
        elif choice == "2":
            display_queue()
        elif choice == "3":
            treat_patient()
        elif choice == "4":
            search_patient()
        elif choice == "5":
            patient_history()
        elif choice == "6":
            statistics()
        elif choice == "7":
            edit_priority()
        elif choice == "8":
            save_data()
            print("Exiting Hospital Emergency Queue System...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
