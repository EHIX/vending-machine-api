# Vending Machine API

## Requirements
Use [pip](https://pip.pypa.io/en/stable/) or [conda](https://docs.conda.io/en/latest/) to install the requirements to run.

```bash

pip install -r requirements.txt

conda install --file requirements.txt

```

## Usage

Start the application.

```bash

python run.py

```

Navigate to http://localhost:8080/

All responses have the form:

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

### Creating a vending machine
**Definition**

GET /build?param=[list of values]

Values passed within query string correspond with the amounts required for each of the eight denominations of coin. Passing a partial sequence, or missing denominations will assign a zero-value entries. Passing more than the prescribed number of denominations will result in surplus values being ignored. The denominations currently used are analogous to British coins: £0.01, £0.02, £0.05, £0.10, £0.20, £0.50, £1.00, £2.00.

**Example**

localhost:8080/build?param=[50, 50, 50, 50, 50, 20, 10, 5]

**Response**

```json
{    
  "data": {
    "cash": {
      "0": {
        "amount": 50,
        "unit": "0.01"
      },
      "1": {
        "amount": 50,
        "unit": "0.02"
      },
      "2": {
        "amount": 50,
        "unit": "0.05"
      },
      "3": {
        "amount": 50,
        "unit": "0.10"
      },
      "4": {
        "amount": 50,
        "unit": "0.20"
      },
      "5": {
        "amount": 20,
        "unit": "0.50"
      },
      "6": {
        "amount": 10,
        "unit": "1.00"
      },
      "7": {
        "amount": 5,
        "unit": "2.00"
      }
    }
  },
  "message": "vending machine successfully built"
}
```

### Get inventory
**Definition**

GET /inventory

The inventory can be returned, but not changed in the current system. The inventory remains an static attribute of the `VendingMachine` class until further requirements surrounding the inventory can be specified. The inventory serves to demonstrate other elements of the system, such as, dispensing the correct amount of change following a successful transaction. The numerical ordering of the items within the inventory corresponds with the parameters passed to make a selection; as described later on.

**Example**

localhost:8080/inventory

**Response**

```json
{
  "data": {
    "inventory": {
      "0": {
        "name": "cola 330ml",
        "price": 0.95
      },
      "1": {
        "name": "lemonade 330ml",
        "price": 0.95
      },
      "2": {
        "name": "water 500ml",
        "price": 1.15
      },
      "3": {
        "name": "orangeade 500ml",
        "price": 1.65
      }
    }
  },
  "message": "inventory items"
}
```

### Get coins available as cash
**Definition**

GET /cash/int:option

Coins deposited within the machine, either from initialisation of as a result of successful transactions, can be returned. Option `0` will return the sum of the coins deposited, and option `1` will display the breakdown of coins available by each denomination (similarly to the response once a vending machine is initially built).

**Example**

localhost:8080/cash/0

**Response**

```json
{
  "data": {
    "cash": {
      "total": "49.00"
    }
  },
  "message": "cash available to vending machine"
}
```

### Get coins collected from current transaction
**Definition**

GET /collection/int:option

Coins deposited within the machine during a transaction. As above, Option `0` will return the sum of the coins currently deposited, and option `1` will display the breakdown of coins available by each denomination.

**Example**

localhost:8080/collected/0

**Response**

```json
{
  "data": {
    "collected": {
      "total": "0.00"
    }
  },
  "message": "cash collected during transaction"
}
```

### Cancel the transaction
**Definition**

GET /terminate

Once a transaction is terminated, any coins currently deposited are returned. Terminate also serves as the only recourse should the vending machine be unable to make the required change before closing a transaction.

**Example**

localhost:8080/terminate

**Response**

```json
{
  "data": {
    "terminate": {
      "error": {
        "coins": null
      }
    }
  },
  "message": "transaction terminated"
}
```

### Adding a coins
**Definition**

GET /add/int:option

Coins are added one at a time, and are passed as options corresponding with the range of prescribed coin denominations. See the <b>Creating a vending machine</b> above for a list of the denominations currently featured.

**Example**

localhost:8080/add/6

**Response**

```json
{
  "data": {
    "add": {
      "success": "1.00"
    }
  },
  "message": "add coin to vending machine"
}
```

### Select and item from inventory
**Definition**

GET /select/int:option

If the appropriate amount has been deposited, the selected item and any change is returned. If change cannot be made, the transaction is cancelled, and any deposited coins are returned. The option parameter corresponds with one of the items within the vending machine inventory. Currently, only one transaction can be handled, meaning that coins must be redeposited to make subsequent purchases.

**Example**

localhost:8080/select/0

**Response**

```json
{
  "data": {
    "select": {
      "success": {
        "transaction": {
          "change": {
            "0": "0.05",
            "1": "1.00"
          },
          "item": "cola 330ml"
        }
      }
    }
  },
  "message": "select item from vending machine"
}
```
