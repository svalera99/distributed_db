# Tasks

### Inserting data to my graph
```bash
CREATE (`Order1`:Order {id: 0, date: "2023-05-05"})<-[:contains]-(:Item {id: 0, name: "PC", price: 500})-[:contains]->(`Order 2`:Order {id: 1, date: "2023-06-06"})<-[:bought]-(John:Customer {name: "John", id: 0})-[:bought]->(`Order1`)<-[:contains]-(:Item {id: 1, name: "Phone", price: 300}),
(:Item {id: 2, name: "Hammer", price: 50})-[:contains]->(`Order 2`)<-[:contains]-(:Item {id: 3, name: "Box", price: 3}),
(John)-[:view]->(:Item {id: 4, name: "Steamdeck", price: 400}),
(:Item {id: 6, name: "Pants", Price: 20})<-[:view]-(Jack:Customer {id: 1, name: "Jack"})-[:bought]->(:Order {id: 2, date: "2024-01-01"})<-[:contains]-(:Item {id: 5, name: "Socks", price: 3}),
(Jack)-[:view]->(:Item {id: 7, name: "Speakers", Price: 100})
```

### 1. All items that are in order, where id is = 1
```bash
MATCH (item: Item)-[:contains]->(order:Order WHERE order.id = 1) RETURN item
```

### 2. Calculate the value of the order, where id is = 1
```bash
MATCH (item: Item)-[:contains]->(order: Order WHERE order.id = 1) RETURN sum(item.price)
```

### 3. Find all orders of customer with id = 0
```bash
MATCH (customer: Customer WHERE customer.id = 0)-[:bought]->(order: Order) RETURN order
```

### 4. Find all items bought by customer with id = 0
```bash
MATCH (customer: Customer WHERE customer.id = 0)-[:bought]->(order: Order)-[:contains]-(item: Item) RETURN item
```

### 5. Sum of all items of customer with id = 0
```bash
MATCH (customer: Customer WHERE customer.id = 0)-[:bought]->(order: Order)-[:contains]-(item: Item) RETURN sum(item.price)
```

### 6. Find how many times each item was bought and sort those values
```bash
MATCH (item: Item)-[cnt:contains]->(order: Order) RETURN item.name, count(cnt) ORDER BY count(cnt) DESC
```

### 7. All items viewed by customer with id = 1
```bash
MATCH (cus: Customer where cus.id = 1)-[v:view]->(item: Item) RETURN item
```

### 8. All items that are in the same order as item with id = 3
```bash
MATCH (item_quer: Item where item_quer.id = 3)-[:contains]->(order: Order)-[:contains]-(item: Item) RETURN item
UNION 
MATCH (item: Item where item.id = 3) RETURN item
```

### 9. Find customer that bought item with id = 0
```bash
MATCH (item: Item WHERE item.id = 0)-[:contains]->(:Order)-[:bought]-(cust:Customer) RETURN collect(distinct cust)
```

### 10. Find items that customer with id = 1 didn't buy
```bash
MATCH (cust: Customer WHERE cust.id = 1)-[:view]->(item: Item) RETURN item
```