from flask import Flask, request ,jsonify
from flask_restful import Resource, Api, reqparse
# from flask_jwt import JWT, jwt_required
# from security import authenticate, identity
import sqlite3

app = Flask(__name__)
# app.secret_key = "SecretKey"
api = Api(app)


# jwt = JWT(app, authenticate, identity)



 

class Item(Resource):
    # @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM product where name =?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.commit()
        connection.close()
        if row:
            item = {'name':row[0],'price':row[1]}
            return {"item":item},200
        else:
            return 404
        #200 = Sucessful, 404 = Not Found

    def post(self,name):
        data = request.get_json() 
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO product VALUES(?,?)"
        cursor.execute(query,(name,data["price"]))
        connection.commit()
        connection.close()
        return {"msg":"sucessfull"},201
        # 201 = Created Sucessfully


    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM product where name =?"
        cursor.execute(query,(name,))
        connection.commit()
        connection.close()
        return {'msg':'Item is Deleted'},201
    
    def put(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument("price", type = float ,required=True, help = "This field cannot be null")
        data = parser.parse_args()
        #data = request.get_json()
        item = next(filter(lambda x : x['name'] == name, items),None)
        if item is None:
            item ={'name':name, 'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item
    
class ItemList(Resource):
    def get(self):
        items = []
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM product"
        result = cursor.execute(query)
        row = result.fetchall()
        connection.commit()
        connection.close()
        for i in range(len(row)):
            item = {'name':row[i][0],'price':row[i][1]}
            if item not in items:
                items.append(item)
        print(row)
        print(item)
        return {"items":items},200

    
    
api.add_resource(Item,"/item/<string:name>")
api.add_resource(ItemList,"/items")
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)