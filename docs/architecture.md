# Architecture

## Overview

The vending machine is structured using an object-oriented design.
The system is divided into several classes, with them all being connected under machine.py and the VendingMachine class.

## Architecture Diagram

[diagram here]

## Components

### VendingMachineCLI
Command Line interface contains:
1. Master Menu: 
    a. Customer menu
        1. View inventory
        2. Insert Money
        3. Purchase
        4. Refund
        5. Back
    b. Administrator menu
        1. View inventory
        2. Insert Money
        3. Purchase
        4. Refund
        5. Restock
        6. Report
        7. Full Inventory Report
        8. Back
    c. Exit

### VendingMachine
This class contains a number of functions:
- initialising slots
- tracks the amount of money spent on contents in the machine
- Validates that a product is in place in the slot mentioned by buyer
- Facilitates purchases by checking if customer is initiated correctly and checking product is in stock, as well as checking if customer has sufficient funds

### Product
- This is where the product class is stored, will take name, sell price and unit stock cost of the product.

### Slot
- Tracks storage of each slot
- Alerts when storage gets down to 0
- Has max capacity also

### Transaction / Reporting
- Tracks information arouind each transactions

## Data Flow

Describe what happens when a customer:

1. Inserts money
    - Money is stored against this customer as the balance in the vending machine at that moment
2. Selects a product / makes a purchase
    - The product is "given" to the customer and the amount is taken from their balance
3. Receives change
    - The change is the remaining balance which the customer can request by selecting the refund option

## Design Decisions

Explain why you chose:
- OOP
    - Each product, slot, customer should be its own onject and have its own class otherwise we would be re-writing a lot of this code
    - Vending machine being a class will also mean it is easy to expand to have multiple vending machines
- separation between CLI and business logic
    - This enables the project to go from being intereacted with from CLI to being a much larger scale
- `Decimal` for monetary values
    - Because you can set the d.p to be 2 easily and keep this consistent across the project 

## Testing Architecture

There are unit tests for each file under the src folder. These ensure that each class and function are working as they should
The CLI tests work across functions and utilise a couple of python tools which enable simulation of CLI.