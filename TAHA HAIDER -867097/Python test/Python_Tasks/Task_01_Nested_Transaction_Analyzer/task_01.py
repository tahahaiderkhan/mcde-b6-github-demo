# Task 01 | Nested Transaction Analyzer

data = [
    {"id": 1, "customer": "Ali", "category": "Food", "amount": 500, "status": "success"},
    {"id": 2, "customer": "Ali", "category": "Travel", "amount": 200, "status": "failed"},
    {"id": 3, "customer": "Sara", "category": "Food", "amount": 700, "status": "success"}
]

customers = {}
ids = []

# Step 1: Calculate customer spending
for x in data:

    if x["id"] in ids:
        raise ValueError("Duplicate Transaction ID")

    ids.append(x["id"])

    name = x["customer"]

    if name not in customers:
        customers[name] = {
            "total": 0,
            "category": {}
        }

    if x["status"] == "success":

        customers[name]["total"] += x["amount"]

        cat = x["category"]

        if cat not in customers[name]["category"]:
            customers[name]["category"][cat] = 0

        customers[name]["category"][cat] += x["amount"]


# Step 2: Find top category
result = []

for name in customers:

    info = customers[name]

    top = None
    highest = 0

    for cat in info["category"]:

        if info["category"][cat] > highest:
            highest = info["category"][cat]
            top = cat

    result.append({
        "customer": name,
        "total": info["total"],
        "top_category": top
    })


# Step 3: Sort by spending and customer name
for i in range(len(result)):

    for j in range(i + 1, len(result)):

        if result[i]["total"] < result[j]["total"]:
            result[i], result[j] = result[j], result[i]

        elif result[i]["total"] == result[j]["total"]:

            if result[i]["customer"] > result[j]["customer"]:
                result[i], result[j] = result[j], result[i]


# Step 4: Assign ranks
for i in range(len(result)):
    result[i]["rank"] = i + 1




# Step 5: Print table

print("Customer | Total | Top Category | Rank")
print("--------------------------------------")

for x in result:
    print(x["customer"], x["total"], x["top_category"], x["rank"])
