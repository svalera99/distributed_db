echo "Starting experiment with items"

echo "------------------------Task 1: Get all data------------------------------------------------"
mongosh "mongodb://mongo:27017/lab_db" --eval "printjson(db['items'].find().toArray())" --quiet

echo "------------------------Task 2: Number of items in certain categories-----------------------"
mongosh "mongodb://mongo:27017/lab_db" --eval "\
    db['items'].aggregate( \
        [{ \
            '\$group': {_id: '\$category', count: {'\$sum': 1}} \
        }] \
    )" --quiet

echo "------------------------Task 3: Number of items categories------------------------------------"
echo "Number of unique categories $(mongosh "mongodb://mongo:27017/lab_db" --eval "db['items'].distinct('category').length" --quiet)" 


echo "------------------------Task 4: List of unique producers----------------------------------------"
echo "List of unqie producers $(mongosh "mongodb://mongo:27017/lab_db" --eval "db['items'].distinct('producer')" --quiet)" 


echo "------------------------Task 5: Items by cretirea-------------------------------------------------"
echo "Task 5.1; model == Model A and 100 <= price <= 200 \
    $(mongosh "mongodb://mongo:27017/lab_db" --eval "db['items'].find( \
            {\$and : [ \
                {'model': 'Model A'}, \
                {'price': {'\$gte': 100}}, \
                {'price': {'\$lte': 200}} \
            ]} \
        )" --quiet)"

echo "Task 5.2; model == Model A or producer == Producer Z \
    $(mongosh "mongodb://mongo:27017/lab_db" --eval "db['items'].find( \
            {\$or : [ \
                {'model': 'Model A'}, \
                {'producer': {'\$eq': 'Producer Z'}} \
            ]} \
        )" --quiet)"

echo "Task 5.3; producer in Producer Z, Producer X \
    $(mongosh "mongodb://mongo:27017/lab_db" --eval "db['items'].find( \
            { 'producer':\
                {\
                    \$in: ['Producer Z', 'Producer X']\
                }\
            } \
        )" --quiet)"


echo "------------------------Task 6: Update certain categories---------------------------------------------"
echo "Task 6.1; setting price to 100 when producer == Producer Y and model == model E \
    $(mongosh "mongodb://mongo:27017/lab_db" --eval "db['items'].updateMany( \
            {\$and : [{'producer': 'Producer Y'}, {'model': 'Model E'}]}, \
            {\$set: {'price': 100}} \
        )" --quiet)"

echo "Task 6.2; adding value has_defect to producer == Producer X or model == model A \
    $(mongosh "mongodb://mongo:27017/lab_db" --eval "db['items'].updateMany( \
            {\$or : [{'producer': 'Producer X'}, {'model': 'Model S'}]}, \
            {\$set: {'has_defect': true}} \
        )" --quiet)"

echo "------------------------Task 7: Find items where has_value exists----------------------------------------"
echo "Task 7; has_values = \
    $(mongosh "mongodb://mongo:27017/lab_db" --eval "db['items'].find( \
            {has_defect: {'\$exists': true}} \
        )" --quiet)"

echo "------------------------Task 8: Incrementing certain values------------------------------------------------"
echo "Task 8; Incrementing where has_defect = true by 100 \
    $(mongosh "mongodb://mongo:27017/lab_db" --eval "db['items'].updateMany( \
            {'has_defect': true}, \
            {'\$inc': {'price': 100}} \
        )" --quiet)"