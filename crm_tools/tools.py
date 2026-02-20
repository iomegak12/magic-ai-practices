from typing import Annotated, Optional
from random import randint, choice
from agent_framework import tool
from pydantic import Field


# In-memory customer storage
customers_db = []
next_customer_id = 11  # Start from 11 since we'll pre-populate 10 records


# Pre-populate with 10 Australian customer records
def initialize_customers():
    """Initialize the database with 10 sample Australian customers."""
    global customers_db, next_customer_id
    
    australian_names = [
        "Liam O'Connor",
        "Charlotte Mitchell",
        "Jack Thompson",
        "Olivia Williams",
        "Noah Fraser",
        "Amelia Robertson",
        "William Chen",
        "Isla Murphy",
        "James Kelly",
        "Mia Anderson"
    ]
    
    australian_cities = [
        "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide",
        "Gold Coast", "Canberra", "Hobart", "Darwin", "Newcastle"
    ]
    
    statuses = ["active", "inactive"]
    
    for i in range(10):
        # Generate email by cleaning the name
        clean_name = australian_names[i].lower().replace(' ', '.').replace("'", '')
        customer = {
            "id": i + 1,
            "name": australian_names[i],
            "city": australian_cities[i],
            "credit_limit": randint(100, 10000),
            "active_status": choice(statuses),
            "email": f"{clean_name}@example.com.au"
        }
        customers_db.append(customer)


# Initialize on module load
initialize_customers()


@tool(approval_mode="never_require")
def create_customer(
    name: Annotated[str, Field(description="The customer's full name")],
    city: Annotated[str, Field(description="The city where the customer is located")],
    credit_limit: Annotated[float, Field(description="The credit limit for the customer (between 100 and 10000)")],
    active_status: Annotated[str, Field(description="The customer's status: 'active' or 'inactive'")],
    email: Annotated[str, Field(description="The customer's email address")],
) -> str:
    """Create a new customer record and return the customer details."""
    global next_customer_id
    
    customer = {
        "id": next_customer_id,
        "name": name,
        "city": city,
        "credit_limit": credit_limit,
        "active_status": active_status.lower(),
        "email": email
    }
    
    customers_db.append(customer)
    next_customer_id += 1
    
    return f"Customer created successfully: ID={customer['id']}, Name={customer['name']}, City={customer['city']}, Credit Limit=${customer['credit_limit']}, Status={customer['active_status']}, Email={customer['email']}"


@tool(approval_mode="never_require")
def get_customer_by_id(
    customer_id: Annotated[int, Field(description="The unique ID of the customer to retrieve")]
) -> str:
    """Get a customer record by their ID."""
    for customer in customers_db:
        if customer["id"] == customer_id:
            return f"Customer found: ID={customer['id']}, Name={customer['name']}, City={customer['city']}, Credit Limit=${customer['credit_limit']}, Status={customer['active_status']}, Email={customer['email']}"
    
    return f"No customer found with ID {customer_id}"


@tool(approval_mode="never_require")
def get_all_customers() -> str:
    """Get all customer records in the database."""
    if not customers_db:
        return "No customers found in the database."
    
    result = f"Total customers: {len(customers_db)}\n\n"
    for customer in customers_db:
        result += f"ID={customer['id']}, Name={customer['name']}, City={customer['city']}, Credit Limit=${customer['credit_limit']}, Status={customer['active_status']}, Email={customer['email']}\n"
    
    return result


@tool(approval_mode="never_require")
def search_customers(
    name: Annotated[Optional[str], Field(description="Search by customer name (partial match, case-insensitive)")] = None,
    email: Annotated[Optional[str], Field(description="Search by email address (partial match, case-insensitive)")] = None,
    city: Annotated[Optional[str], Field(description="Search by city (partial match, case-insensitive)")] = None,
) -> str:
    """Search for customers by name, email, or city. All search criteria are optional and use partial, case-insensitive matching."""
    
    if not any([name, email, city]):
        return "Please provide at least one search criterion (name, email, or city)."
    
    results = []
    
    for customer in customers_db:
        match = True
        
        if name and name.lower() not in customer["name"].lower():
            match = False
        
        if email and email.lower() not in customer["email"].lower():
            match = False
        
        if city and city.lower() not in customer["city"].lower():
            match = False
        
        if match:
            results.append(customer)
    
    if not results:
        search_criteria = []
        if name:
            search_criteria.append(f"name containing '{name}'")
        if email:
            search_criteria.append(f"email containing '{email}'")
        if city:
            search_criteria.append(f"city containing '{city}'")
        
        return f"No customers found matching: {', '.join(search_criteria)}"
    
    result_text = f"Found {len(results)} customer(s):\n\n"
    for customer in results:
        result_text += f"ID={customer['id']}, Name={customer['name']}, City={customer['city']}, Credit Limit=${customer['credit_limit']}, Status={customer['active_status']}, Email={customer['email']}\n"
    
    return result_text
