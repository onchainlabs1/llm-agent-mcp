import json
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()
Faker.seed(42)
random.seed(42)

DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

# --- Products ---
product_names = [
    'Laptop', 'Smartphone', 'Tablet', 'Monitor', 'Keyboard',
    'Mouse', 'Headphones', 'Webcam', 'Printer', 'Router'
]
products = []
for i, name in enumerate(product_names):
    products.append({
        "sku": f"SKU-{i+1:03d}",
        "name": name,
        "price": round(random.uniform(50, 2000), 2)
    })
with open(os.path.join(DATA_DIR, 'products.json'), 'w') as f:
    json.dump(products, f, indent=2)

# --- Clients ---
clients = []
for i in range(30):
    clients.append({
        "id": f"cli{i+1:03d}",
        "name": fake.name(),
        "email": fake.email(),
        "company": fake.company(),
        "phone": fake.phone_number(),
        "balance": round(random.uniform(100, 10000), 2),
        "created_at": fake.date_between(start_date='-2y', end_date='today').isoformat(),
        "status": random.choice(["active", "inactive"])
    })
with open(os.path.join(DATA_DIR, 'clients.json'), 'w') as f:
    json.dump(clients, f, indent=2)

# --- Orders ---
order_statuses = ["pending", "shipped", "delivered", "cancelled"]
orders = []
for i in range(100):
    client = random.choice(clients)
    order_date = fake.date_between(start_date=client["created_at"], end_date='today')
    num_items = random.randint(1, 4)
    items = []
    total = 0.0
    for _ in range(num_items):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        unit_price = product["price"]
        items.append({
            "product": product["name"],
            "sku": product["sku"],
            "quantity": quantity,
            "unit_price": unit_price
        })
        total += quantity * unit_price
    orders.append({
        "id": f"ORD-{order_date.strftime('%Y%m%d')}-{i+1:03d}",
        "client_id": client["id"],
        "total": round(total, 2),
        "status": random.choice(order_statuses),
        "created_at": order_date.isoformat(),
        "items": items
    })
with open(os.path.join(DATA_DIR, 'orders.json'), 'w') as f:
    json.dump(orders, f, indent=2)

print("Synthetic CRM/ERP data generated in 'data/'!") 