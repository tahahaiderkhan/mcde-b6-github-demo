# Task 10 – CSV Inventory

import csv

inventory = {}

# Read inventory
with open("inventory.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        inventory[row["sku"]] = {
            "name": row["name"],
            "quantity": int(row["quantity"])
        }


rejected = []

# Read movements
with open("movements.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        sku = row["sku"]
        movement = row["type"]
        units = int(row["units"])

        if sku not in inventory:
            rejected.append(row)

        elif units <= 0:
            rejected.append(row)

        elif movement == "IN":
            inventory[sku]["quantity"] += units

        elif movement == "OUT":

            if inventory[sku]["quantity"] >= units:
                inventory[sku]["quantity"] -= units

            else:
                rejected.append(row)

        else:
            rejected.append(row)


# Save updated inventory
with open("updated_inventory.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow(["sku", "name", "quantity"])

    for sku in inventory:

        writer.writerow([
            sku,
            inventory[sku]["name"],
            inventory[sku]["quantity"]
        ])


# Save rejected movements
with open("rejected_movements.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow(["sku", "type", "units"])

    for row in rejected:

        writer.writerow([
            row["sku"],
            row["type"],
            row["units"]
        ])


print("Inventory updated")
print("P01 Stock:", inventory["P01"]["quantity"])
print("Rejected:", len(rejected))
