import streamlit as st
import pandas as pd


inventory = pd.DataFrame(columns=['Item ID', 'Name', 'Price', 'Quantity'])


# Function to load inventory data from an Excel file
def load_inventory(filename):
    try:
        inventory_data = pd.read_excel(filename)
        inventory_data = inventory_data.fillna('')
        return inventory_data
    except Exception as e:
        st.error(f"Error loading inventory data: {e}")
        return pd.DataFrame(columns=['Item ID', 'Name', 'Price', 'Quantity'])


# Function to display inventory
def display_inventory():
    st.header("Inventory:")
    st.table(inventory)


# Function to make a sale
def make_sale():
    display_inventory()
    total_price = 0
    sale_items = {}

    while True:
        # st.text_input("Enter item ID to add to the sale (or 'done' to finish):", key="item_id_input")
        item_id = st.text_input("Enter item ID to add to the sale (or 'done' to finish):", key="item_id")
        if item_id.lower() == 'done':
            break

        try:
            quantity = st.number_input(f"Enter quantity for {item_id}:", key = "quantity", min_value=1)
        except ValueError:
            st.error("Please enter a valid quantity.")
            continue

        item_data = inventory[inventory['Item ID'] == item_id]

        if not item_data.empty:
            available_quantity = item_data['Quantity'].values[0]
            if quantity <= available_quantity:
                item_price = item_data['Price'].values[0]
                total_price += item_price * quantity

                # Update the inventory
                inventory.loc[inventory['Item ID'] == item_id, 'Quantity'] -= quantity

                # Record the sale
                sale_items[item_id] = {'name': item_data['Name'].values[0], 'quantity': quantity,
                                       'price': item_price}
            else:
                st.error(f"Insufficient quantity in inventory. Available quantity: {available_quantity}")
        else:
            st.error("Invalid selection. Item not found in inventory.")

    if sale_items:
        st.header("Sale Summary:")
        for item_id, item_data in sale_items.items():
            st.write(f"{item_data['name']} - Quantity: {item_data['quantity']} - Price: ${item_data['price']} each")

        st.write(f"Total Price: ${total_price}")



def increase_inventory():
    global inventory
    display_inventory()
    item_id2 = st.text_input("Enter item ID to increase quantity:", key="item_id2")
    quantity_to_add = st.number_input("Enter quantity to add:", min_value=1)

    item_data = inventory[inventory['Item ID'] == item_id2]

    if not item_data.empty:
        # Increase the quantity in the inventory
        inventory.loc[inventory['Item ID'] == item_id2, 'Quantity'] += quantity_to_add
        st.success(f"{quantity_to_add} {item_data['Name'].values[0]} added to the inventory.")
    else:
        st.error("Item not found in inventory.")


def main():
    global inventory  # Declare inventory as a global variable
    st.title("Point of Sale System")

    inventory_filename = 'inventory.xlsx'  # Specify the Excel file containing inventory data
    inventory = load_inventory(inventory_filename)

    menu_choice = st.sidebar.selectbox("Menu", ["Make a Sale", "Display Inventory", "Increase Inventory"])

    if menu_choice == "Make a Sale":
        make_sale()
    elif menu_choice == "Display Inventory":
        display_inventory()
    elif menu_choice == "Increase Inventory":
        increase_inventory()


if __name__ == "__main__":
    main()