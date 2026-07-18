from vending_machine import Product

name = input("Product name: ").strip()
sell_price = input("Sell price: ")
unit_stock_cost = input("Unit stock cost: ")

P = Product(name="fill", sell_price=5, unit_stock_cost=5)

try:
    product = Product(name, sell_price, unit_stock_cost)
except ValueError as exc:
    print("Invalid product:", exc)
else:
    print("name:", product.name)
    print("sellPrice:", product.sell_price)
    print("unit_stock_cost:", product.unit_stock_cost)
