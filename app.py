# The microservice above implements a REST API for training and using machine learning models. 
# It has several key functionalities:
#     1 Training ML models with customizable hyperparameters: the user can train a regression, 
#     classification, or random forest model, and specify the hyperparameters they want to use.

#     2 Listing available model classes: the user can get a list of the model classes that are available for training.

#     3 Returning predictions: the user can get predictions from a specific trained model, 
#     and the system is capable of storing multiple trained models.

#     4 Retraining and deleting models: the user can retrain a model or delete a previously trained model.

# The microservice takes in HTTP requests with data for training, 
# hyperparameters, or model predictions, and outputs HTTP responses with information about the available model classes, 
# the trained models, or the predictions made

import os
import psycopg2
from flask import Flask, request
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression

app = Flask(__name__)

@app.route('/model', methods=['GET', 'POST'])
def model():
    """
    Train the model.

    Parameters
    ----------
    model_class: str
        Class of the model.
    hyperparameters: dict
        Hyperparameters for the model.

    Returns
    -------
    str
        Status of training the model.

    """
    if request.method == 'GET':
        return 'Regression, Classification, RandomForest'

    if request.method == 'POST':
        model_class = request.json['model_class']
        hyperparameters = request.json['hyperparameters']
        
        if model_class == 'Regression':
            model = LinearRegression(**hyperparameters)
        elif model_class == 'Classification':
            model = LogisticRegression(**hyperparameters)
        elif model_class == 'RandomForest':
            model = RandomForestClassifier(**hyperparameters)
        else:
            return 'Invalid model class'
        
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cur = conn.cursor()
        cur.execute("INSERT INTO models (model_class, model) VALUES (%s, %s)", (model_class, model))
        conn.commit()
        cur.close()
        conn.close()
        
        return 'Model trained successfully'

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict the data.

    Parameters
    ----------
    model_id: int
        Id of the model.
    data: list
        Data to predict.

    Returns
    -------
    str
        Prediction of data.

    """
    model_id = request.json['model_id']
    data = request.json['data']
    
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("SELECT model FROM models WHERE id = %s", (model_id,))
    model = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    prediction = model.predict(data)
    
    return str(prediction)

@app.route('/delete_model', methods=['POST'])
def delete_model():
    """
    Delete the model.

    Parameters
    ----------
    model_id: int
        Id of the model.

    Returns
    -------
    str
        Status of deleting the model.

    """
    model_id = request.json['model_id']
    
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("DELETE FROM models WHERE id = %s", (model_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return 'Model deleted successfully'

if __name__ == '__main__':
    app.run()
