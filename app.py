import os
import psycopg2
from flask import Flask, request
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression

app = Flask(__name__)

@app.route('/model', methods=['GET', 'POST'])
def model():
    if request.method == 'GET':
        # return the list of available model classes
        return 'Regression, Classification, RandomForest'

    if request.method == 'POST':
        # get the parameters from the request
        model_class = request.json['model_class']
        hyperparameters = request.json['hyperparameters']
        
        # train the model based on the given class and hyperparameters
        if model_class == 'Regression':
            model = LinearRegression(**hyperparameters)
        elif model_class == 'Classification':
            model = LogisticRegression(**hyperparameters)
        elif model_class == 'RandomForest':
            model = RandomForestClassifier(**hyperparameters)
        else:
            return 'Invalid model class'
        
        # store the model in the database
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cur = conn.cursor()
        cur.execute("INSERT INTO models (model_class, model) VALUES (%s, %s)", (model_class, model))
        conn.commit()
        cur.close()
        conn.close()
        
        return 'Model trained successfully'

@app.route('/predict', methods=['POST'])
def predict():
    # get the model_id and the data from the request
    model_id = request.json['model_id']
    data = request.json['data']
    
    # retrieve the model from the database
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("SELECT model FROM models WHERE id = %s", (model_id,))
    model = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    # make a prediction using the model
    prediction = model.predict(data)
    
    return str(prediction)

@app.route('/delete_model', methods=['POST'])
def delete_model():
    # get the model_id from the request
    model_id = request.json['model_id']
    
    # delete the model from the database
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("DELETE FROM models WHERE id = %s", (model_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return 'Model deleted successfully'

if __name__ == '__main__':
    app.run()
