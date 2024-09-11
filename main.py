import json

def load_data():
    try:
        with open('store_data.json', 'r') as file:
            data = json.load(file)
        return {
            'products': {name: {**product, 'price': float(str(product['price'])), 'cost': float(str(product['cost']))}
                         for name, product in data['products'].items()},
            'sales': data['sales']
        }
    except FileNotFoundError:
        return {'products': {}, 'sales': []}

def save_data(data):
    with open('store_data.json', 'w') as file:
        json.dump({
            'products': {name: {**product, 'price': str(product['price']), 'cost': str(product['cost'])}
                         for name, product in data['products'].items()},
            'sales': data['sales']
        }, file, indent=2)

def add_product(data):
    """Add a new product or update existing product quantity."""
    name = input("Nome del prodotto: ").lower()
    try:
        quantity = int(input("Quantità: "))
        if quantity <= 0:
            raise ValueError("La quantità deve essere un numero positivo.")
        
        if name in data['products']:
            data['products'][name]['quantity'] += quantity
            print(f"AGGIUNTO: {quantity} X {name}")
        else:
            cost = float(input("Prezzo di acquisto: "))
            price = float(input("Prezzo di vendita: "))
            if cost <= 0 or price <= 0:
                raise ValueError("I prezzi devono essere numeri positivi.")
            data['products'][name] = {'quantity': quantity, 'cost': cost, 'price': price}
            print(f"AGGIUNTO: {quantity} X {name}")
    except ValueError as e:
        print(f"Errore: {str(e)}")

def list_products(data):
    """List all products in the inventory."""
    print("PRODOTTO\tQUANTITA'\tPREZZO")
    for name, product in data['products'].items():
        print(f"{name}\t{product['quantity']}\t€{product['price']:.2f}")

def register_sale(data):
    """Register a sale of one or more products."""
    sale = []
    total = float('0')
    while True:
        name = input("Nome del prodotto: ").lower()
        if name not in data['products']:
            print("Prodotto non trovato.")
            if input("Vuoi cercare un altro prodotto ? (si/no): ").lower() != 'si':
                break
            continue
        try:
            quantity = int(input("Quantità: "))
            if quantity <= 0:
                raise ValueError("La quantità deve essere un numero positivo.")
            if quantity > data['products'][name]['quantity']:
                print("Quantità non disponibile.")
                continue
            price = data['products'][name]['price']
            subtotal = price * quantity
            sale.append({'name': name, 'quantity': quantity, 'price': price})
            total += subtotal
            data['products'][name]['quantity'] -= quantity
            print(f"- {quantity} X {name}: €{price:.2f}")
            if input("Aggiungere un altro prodotto ? (si/no): ").lower() != 'si':
                break
        except ValueError as e:
            print(f"Errore: {str(e)}")
    
    if sale:
        data['sales'].append({'items': sale, 'total': total})
        print("VENDITA REGISTRATA")
        print(f"Totale: €{total:.2f}")

def show_profits(data):
    """Calculate and display gross and net profits."""
    gross_profit = sum(sale['total'] for sale in data['sales'])
    net_profit = gross_profit - sum(
        sum(item['quantity'] * data['products'][item['name']]['cost'] for item in sale['items'])
        for sale in data['sales']
    )
    print(f"Profitto: lordo=€{gross_profit:.2f} netto=€{net_profit:.2f}")

def show_help():
    """Display available commands."""
    print("I comandi disponibili sono i seguenti:")
    print("aggiungi: aggiungi un prodotto al magazzino")
    print("elenca: elenca i prodotto in magazzino")
    print("vendita: registra una vendita effettuata")
    print("profitti: mostra i profitti totali")
    print("aiuto: mostra i possibili comandi")
    print("chiudi: esci dal programma")

def main():
    data = load_data()
    commands = {
        'aggiungi': add_product,
        'elenca': list_products,
        'vendita': register_sale,
        'profitti': show_profits,
        'aiuto': show_help
    }

    while True:
        command = input("Inserisci un comando: ").lower()
        if command == 'chiudi':
            print("Bye bye")
            break
        elif command in commands:
            if command != "aiuto":  
                commands[command](data)
            else:
                commands[command]()

        else:
            print("Comando non valido")
            show_help()
        save_data(data)

if __name__ == "__main__":
    main()
