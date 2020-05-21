from vending import VendingMachine

def main():
    standard = [50, 50, 50, 50, 50, 20, 10, 5]
    vm = VendingMachine(standard)
    vm.print_total(v=1)
    vm.print_collected(v=1)
    vm.print_inventory()
    vm.insert_coins()
    vm.terminate()
    vm.print_collected(v=1)
    vm.print_total(v=1)
    vm.insert_coins()
    vm.select(1)
    vm.print_total(v=1)
    vm.print_collected(v=1)

if __name__ == "__main__":
    main()
