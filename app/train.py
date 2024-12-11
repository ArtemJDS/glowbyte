import mlflow
from mlflow.models import infer_signature
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import sys
import os


logmodel_params = {
    "solver": "lbfgs",
    "max_iter": 1000,
    "multi_class": "auto",
    "random_state": 8888,
}

INDEX_TO_SPECIES = {
                    0: 'setosa', 
                    1: 'versicolor',
                    2: 'virginica'
                    }


def get_iris_data():
    X, y = datasets.load_iris(return_X_y=True)
    return train_test_split( X, y, test_size=0.2, random_state=42)

def get_trained_logmodel(X_train, y_train):
    lr = LogisticRegression(**logmodel_params)
    lr.fit(X_train, y_train)
    return lr

def train_single_model():

    X_train, X_test, y_train, y_test = get_iris_data()
    lr = get_trained_logmodel(X_train, y_train)
    accuracy = accuracy_score(y_test, lr.predict(X_test))

    mlflow.set_tracking_uri(uri=f'http://127.0.0.1:{os.environ["SERVER_PORT"]}')
    mlflow.set_experiment("glowbyte iris")
    with mlflow.start_run():

        mlflow.log_params(logmodel_params)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.set_tag("Training Info", "Basic LR model for iris data")
        signature = infer_signature(X_train, lr.predict(X_train))
        model_info = mlflow.sklearn.log_model(
            sk_model=lr,
            artifact_path="iris_model",
            signature=signature,
            input_example=X_train,
            registered_model_name="default_iris_model",
        )

    model_uri = model_info.model_uri
    os.environ['MODEL_URI'] = model_uri

