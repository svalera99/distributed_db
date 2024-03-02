echo "Starting experiment with orders"

echo "------------------------Task 1: Get all data------------------------------------------------"
mongosh "mongodb://mongo:27017/lab_db" --eval "printjson(db['orders'].find().toArray())" --quiet

echo "------------------------Task 2: All items with total_sum greater than 100-------------------"
mongosh "mongodb://mongo:27017/lab_db" --eval "printjson(db['orders'].find({\
            total_sum: {'\$gte': 100}\
        }\
    ))" --quiet


echo "------------------------Task 3: All orders done by Valery Pupko--------------------------------"
mongosh "mongodb://mongo:27017/lab_db" --eval "printjson(db['orders'].find(\
        {'\$and':[\
            {'customer.name' : 'Valery'},\
            {'customer.surname' : 'Pupko'}\
        ]}\
    ))" --quiet

echo "------------------------Task 4: All orders with id 65dd0bc901d78a20ef981b71-----------------------"
mongosh "mongodb://mongo:27017/lab_db" --eval "printjson(db['orders'].find(\
        {'items_id': '65dd0bc901d78a20ef981b71'}\
    ))" --quiet

echo "------------------------Task 5: Add certain item to the order and increment total_sum by 100---------"
mongosh "mongodb://mongo:27017/lab_db" --eval "printjson(db['orders'].updateMany(\
        {'items_id': '65dd0bc901d78a20ef981b5c'},\
        {\
            '\$push': {'items_id' : '65dd0bc901d78a20ef981b57'},\
            '\$inc': {'total_sum': 100}
        }
    ))" --quiet

echo "------------------------Task 6: Print number of items in certain order---------"
mongosh "mongodb://mongo:27017/lab_db" --eval "db['orders'].aggregate(\
        [\
            {\
                '\$match': {\
                    "order_number": 3140401\
                }\
            },\
            {\
                '\$project': {\
                    count: {'\$size': '\$items_id'}\
                }\
            }\
        ]\
    )" --quiet

echo "------------------------Task 7: Orders with total_sum more than 5000-------------"
mongosh "mongodb://mongo:27017/lab_db" --eval "db['orders'].find(\
        {\
            'total_sum': {'\$gte': 5000}\
        },\
        {\
            'customer': 1, 'payment.cardId': 1, _id: 0 \
        }\
    )" --quiet

echo "------------------------Task 9: Renaming each order's name-------------------------"
mongosh "mongodb://mongo:27017/lab_db" --eval "db['orders'].updateMany(\
        {},\
        {\
            '\$set': {'customer.name': 'Vasyl'} \
        }\
    )" --quiet

# echo "------------------------Task 9: Renaming each order's name-------------------------"
# mongosh "mongodb://mongo:27017/lab_db" --eval "db['orders'].aggregate(\
#         [\
#             {\
#                 '\$match': {\
#                     '\$and': [\
#                         {'customer.name': 'Vasyl'},\
#                         {'customer.surname': 'Pupko'}\
#                     ]\
#                 }\
#             },\
#             {\
#                 '\$lookup': {\
#                     from: 'items',\
#                     localField: 'items_id',\
#                     foreignField: '_id',\
#                     as: 'item_details'\
#                 }\
#             }\
#         ]\
#     )" --quiet


# echo "------------------------Task 10: Adding collection-------------------------"
# mongosh "mongodb://mongo:27017/lab_db" --eval "db.createCollection('my_capped_collection', { capped : true, size : 5242880, max : 5 } )" --quiet
# mongosh "mongodb://mongo:27017/lab_db" --eval "db['orders'].aggregate([\
#         { \$sort: { "date": -1 } },\
#         { \$limit: 1 },\
#         { \$out: "my_capped_collection" }
#     ])"