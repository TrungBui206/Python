from collections import defaultdict, deque

class Product:
    def __init__(self, product_id, name, brand, price, quantity, category):
        self.product_id = product_id  
        self.name = name.strip()  
        self.brand = brand.strip() 
        self.price = price  
        self.quantity = quantity 
        self.category = category.strip() 

    def __str__(self):
        return f"Ma: {self.product_id}, Ten: {self.name},Thuong hieu: {self.brand}, Gia: {self.price}, So luong: {self.quantity}, Loai: {self.category}"

class Inventory:
    def __init__(self):
        self.products = {} 
        self.category_index = defaultdict(set)  
        self.brand_index = defaultdict(set) 
        self.order = []  

    def add_product(self, product):
        if product.product_id in self.products:
            print("San pham da ton tai.")
            return
        self.products[product.product_id] = product
        self.category_index[product.category.lower()].add(product.product_id)
        self.brand_index[product.brand.lower()].add(product.product_id)
        self.order.append(product.product_id)

    def remove_product(self, product_id):
        if product_id in self.products:
            p = self.products.pop(product_id)
            self.category_index[p.category.lower()].remove(product_id)
            self.brand_index[p.brand.lower()].remove(product_id)
            self.order.remove(product_id)
            return True
        print("San pham khong ton tai.")
        return False

    def search_by_category(self, category):
        ids = self.category_index[category.strip().lower()]
        return [self.products[id] for id in ids]

    def search_by_brand(self, brand):
        ids = self.brand_index[brand.strip().lower()]
        return [self.products[id] for id in ids]

    def check_quantity(self, product_id): 
        if product_id in self.products:
            return self.products[product_id].quantity 
        return None 
    
    def reduce_quantity(self, product_id, amount):
        if product_id in self.products: 
            product = self.products[product_id]
            if product.quantity >= amount: 
                product.quantity -= amount
                return True 
            else:
                print("Khong du so luong trong kho.")
                return False
        print("San pham khong ton tai.")
        return False

    def display_all(self):
        if not self.order:
            print("Kho hang rong.")
            return
        for id in self.order:
            print(self.products[id])

class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id  
        self.name = name.strip()
        self.cart = {}
        self.total = 0 
    
    def add_to_cart(self, inventory, product_id, quantity):
        available = inventory.check_quantity(product_id)  
        if available is None:
            print("San pham khong ton tai.")
            return False  
        if available < quantity:
            print("Khong du so luong trong kho.")
            return False
        self.cart[product_id] = self.cart.get(product_id, 0) + quantity
        print("Da them vao gio hang.")
    
    def checkout(self, inventory):
        total = 0
        print(f"Hoa don mua hang cua {self.name} ")
        for pid, qty in self.cart.items():
            product = inventory.products.get(pid) 
            if product and inventory.reduce_quantity(pid, qty):
                cost = product.price * qty
                total += cost
                print(f"{product.name} x {qty} = {cost} VND")
            else:
                print(f"Khong the mua {product.name} do khong du so luong.")
        self.total = total
        print(f"Tong cong: {self.total} VND")
        print("Cam on ban da mua hang!")
        self.cart.clear()

class CustomerQueue:
    def __init__(self):
        self.queue = deque()

    def add_customer(self, customer):
        self.queue.append(customer)
        print(f"Khach hang {customer.name} da duoc them vao hang doi.")
    
    def next_customer(self):
        if self.queue:
            return self.queue.popleft()
        print("Khong con khach hang nao trong hang doi.")
        return None

    def show_queue(self):
        if not self.queue:
            print("Hang doi khach hang rong.")
            return
        print("Danh sach khach hang trong hang doi:")
        for customer in self.queue:
            print(f"Ma khach hang: {customer.customer_id}, Ten: {customer.name}")
    
    def serve_next_customer(self, inventory):
        customer = self.next_customer()
        if not customer:
            return

        print(f"Dang phuc vu khach hang: {customer.name}")
        while True:
            pid = input("Nhap ma san pham can mua (hoac 'X' de ket thuc): ").strip()
            if pid.lower() == 'x':
                customer.checkout(inventory)
                break
            qty = int(input("Nhap so luong: ").strip())
            customer.add_to_cart(inventory, pid, qty)



def main():
    inventory = Inventory() 
    queue = CustomerQueue()

    while True:
        print("\n=== He thong sieu thi ===")
        print("1. Quan ly hang hoa")
        print("2. Quan ly khach hang")
        print("3. Thoat")
        choice = input("Nhap lua chon: ").strip()

        if choice == '1':
            while True:
                print("\n=== Quan ly hang hoa sieu thi ===")
                print("1. Them san pham")
                print("2. Bot san pham")
                print("3. Tim theo loai hang")
                print("4. Tim theo thuong hieu")
                print("5. Kiem tra so luong theo ma")
                print("6. Hien thi tat ca san pham")
                print("7. Quay lai menu chinh")
                choice = input("Nhap lua chon: ").strip()
        
                if choice == '1':
                    pid = input("Ma san pham: ").strip()
                    name = input("Ten: ").strip()
                    brand = input("Thuong hieu: ").strip()
                    price = float((input("Gia: ")).strip())
                    qty = int((input("So luong: ")).strip())
                    cat = input("Loai hang (quan ao, thuc pham, do dien tu,...): ").strip()
                    product = Product(pid, name, brand, price, qty, cat)
                    inventory.add_product(product)
                    print("San pham da them.")

                elif choice == '2':
                    pid = input("Ma san pham can bot: ").strip()
                    if inventory.remove_product(pid):
                        print("San pham da bot.")
        
                elif choice == '3':
                    cat = input("Loai hang can tim: ").strip()
                    results = inventory.search_by_category(cat)
                    if results:
                            print("San pham tim thay:")
                            for p in results:
                                print(p)
                    else:
                        print("Khong tim thay san pham.")
        
                elif choice == '4':
                    brand = input("Thuong hieu can tim: ").strip()
                    results = inventory.search_by_brand(brand)
                    if results:
                        print("San pham tim thay:")
                        for p in results:
                            print(p)
                    else:
                        print("Khong tim thay san pham.")
        
                elif choice == '5':
                    pid = input("Ma san pham: ").strip()
                    qty = inventory.check_quantity(pid)
                    if qty is not None:
                        print(f"So luong con lai: {qty}")
        
                elif choice == '6':
                    print("Tat ca san pham:")
                    inventory.display_all()
                
                elif choice == '7':
                    break
                else:
                    print("Lua chon khong hop le.")
        
        elif choice == '2':
            while True:
                print("\n=== Quan ly khach hang ===")
                print("1. Them khach hang vao hang doi")
                print("2. Phuc vu khach hang ")
                print("3. Hien thi hang doi khach hang")
                print("4. Quay lai menu chinh")
                choice = input("Nhap lua chon: ").strip()
        
                if choice == '1':
                    cid = input("Ma khach hang: ").strip()
                    name = input("Ten khach hang: ").strip()
                    customer = Customer(cid, name)
                    queue.add_customer(customer)
        
                elif choice == '2':
                    queue.serve_next_customer(inventory)
        
                elif choice == '3':
                    queue.show_queue()
        
                elif choice == '4':
                    break
                else:
                    print("Lua chon khong hop le.")


        elif choice == '3':    
            print("Thoat chuong trinh.")
            break
        else:
            print("Lua chon khong hop le.")

if __name__ == "__main__":
    main()
