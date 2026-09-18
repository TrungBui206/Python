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
        #Kiểm tra số lượng sản phẩm trong kho dựa trên mã sản phẩm
        if product_id in self.products:
            return self.products[product_id].quantity #nếu sản phẩm tồn tại, trả về số lượng hiện có
        return None # nếu sản phẩm không tồn tại, trả về None
    
    def reduce_quantity(self, product_id, amount):
        #Giảm số lượng sản phẩm trong kho sau khi khách hàng mua
        if product_id in self.products: #nếu sản phẩm tồn tại trong kho
            product = self.products[product_id]
            if product.quantity >= amount: 
                #kiểm tra nếu số lượng hiện có đủ để giảm, product.quantity là số lượng sản phẩm hiện có trong kho, amount là số lượng khách hàng muốn mua
                product.quantity -= amount
                return True #nếu giảm thành công, trả về True
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
    #Khởi tạo lớp khách hàng lưu trữ các thông tin khách hàng như mã khách hàng và tên
    def __init__(self, customer_id, name):
        self.customer_id = customer_id  
        self.name = name.strip()
        self.cart = {}# tạo giỏ hàng rỗng để lưu trữ các sản phẩm mà khách hàng muốn mua bằng phương thức dict đã import ở trên
        self.total = 0 # tổng tiền thanh toán ban đầu là 0
    
    def add_to_cart(self, inventory, product_id, quantity):
        #Thêm sản phẩm vào giỏ hàng của khách hàng, liên kết với inventory để kiểm tra số lượng sản phẩm trong kho
        available = inventory.check_quantity(product_id)  
        #Kiểm tra nếu sản phẩm tồn tại trong kho thông qua id trong hàm check_quantity ở lớp Inventory
        if available is None:
            print("San pham khong ton tai.")
            return False  
        if available < quantity:
            print("Khong du so luong trong kho.")
            return False
        self.cart[product_id] = self.cart.get(product_id, 0) + quantity
        #nếu sản phẩm đã có trong giỏ hàng, tăng số lượng, nếu chưa có, thêm sản phẩm với số lượng mới
        print("Da them vao gio hang.")
    
    def checkout(self, inventory):
        #Thanh toán giỏ hàng của khách hàng, liên kết với inventory để giảm số lượng sản phẩm trong kho
        total = 0
        print(f"Hoa don mua hang cua {self.name} ")
        for pid, qty in self.cart.items():
            #Lấy thông tin sản phẩm từ kho hàng dựa trên mã sản phẩm, 
            product = inventory.products.get(pid) #lấy đối tượng sản phẩm từ kho thông qua mã 
            if product and inventory.reduce_quantity(pid, qty):
                #kiểm tra xem sản phẩm có tồn tại và giảm số lượng trong kho thành công
                cost = product.price * qty
                total += cost
                print(f"{product.name} x {qty} = {cost} VND")
            else:
                #nếu sản phẩm không tồn tại hoặc không đủ số lượng trong kho
                print(f"Khong the mua {product.name} do khong du so luong.")
        self.total = total
        print(f"Tong cong: {self.total} VND")
        print("Cam on ban da mua hang!")
        self.cart.clear()
        #Xoá giỏ hàng sau khi thanh toán xong

class CustomerQueue:
    #Quản lý hàng đợi khách hàng sử dụng deque(hàng đợi) để thêm và phục vụ khách hàng theo thứ tự FIFO
    def __init__(self):
        self.queue = deque()

    def add_customer(self, customer):
        self.queue.append(customer)
        print(f"Khach hang {customer.name} da duoc them vao hang doi.")
    
    def next_customer(self):
        if self.queue:
            return self.queue.popleft()#pop là lấy và xóa phần tử đầu tiên của hàng đợi, rồi đẩy phần từ tiếp theo lên đầu
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
        #Hàm phục vụ khách hàng tiếp theo. Ban đầu là hàng sẽ rỗng và khi thêm vào, sẽ tự động lấy khách hàng đầu tiên trong hàng đợi khi mình thêm vào.
        #Tiếp theo là sẽ xóa đi khách hàng đó khỏi hàng đợi và phục vụ họ.
        customer = self.next_customer()
        #khách hàng sẽ lấy từ hàng đợi thông qua hàm next_customer đã định nghĩa ở trên
        if not customer:
            #Nếu không có khách hàng nào trong hàng đợi, hàm sẽ kết thúc và không thực hiện gì thêm
            return

        print(f"Dang phuc vu khach hang: {customer.name}")
        while True:
            pid = input("Nhap ma san pham can mua (hoac 'X' de ket thuc): ").strip()
            if pid.lower() == 'x':
                customer.checkout(inventory)
                #Khi khách hàng nhập 'X', hàm checkout sẽ được gọi để thanh toán giỏ hàng của khách hàng và giỏ hàng sẽ được thanh toán
                break
            qty = int(input("Nhap so luong: ").strip())
            customer.add_to_cart(inventory, pid, qty)
            # customer.add_to_cart sẽ được gọi để thêm sản phẩm vào giỏ hàng của khách hàng



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
                    #khi chọn phục vụ khách hàng, hàm serve_next_customer sẽ được gọi để phục vụ khách hàng tiếp theo trong hàng đợi
                    #inventory được truyền vào để quản lý kho hàng trong quá trình phục vụ khách hàng
        
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