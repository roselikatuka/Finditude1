from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine
import pandas as pd
from config import DATABASE_CONFIG

app = Flask(__name__)
api = Api(app)

DATABASE_URL = f"mysql+pymysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"
engine = create_engine(DATABASE_URL)

class Home(Resource):
    def get(self):
        return {"message": "Flask backend is running!"}

class DemoAPI(Resource):
    def get(self):
        
        query_type = request.args.get("type", "all")  

        if query_type == "all":
            query = "SELECT * FROM demo LIMIT 5;"  
            df = pd.read_sql(query, engine)
        elif query_type == "recommend":
            query = "SELECT * FROM demo;"
            df = pd.read_sql(query, engine)

            if df.empty:
                return jsonify({"message": "No recommendations available"})

            df = df.sample(n=2, replace=False) if len(df) >= 5 else df
        else:
            return jsonify({"error": "Invalid type parameter. Use 'all' or 'recommend'."})

        return jsonify(df.to_dict(orient="records"))


api.add_resource(Home, "/")
api.add_resource(DemoAPI, "/api/demo")  

if __name__ == "__main__":
    app.run(debug=True)
