from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Load and preprocess dataset
data = pd.read_csv("E:/Programming/Projects/Diabetes_Predict/diabetes.csv")
X = data.drop("Outcome", axis=1)
y = data["Outcome"]

# Train model
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        try:
            input_features = [
                float(request.form["Pregnancies"]),
                float(request.form["Glucose"]),
                float(request.form["BloodPressure"]),
                float(request.form["SkinThickness"]),
                float(request.form["Insulin"]),
                float(request.form["BMI"]),
                float(request.form["DiabetesPedigreeFunction"]),
                float(request.form["Age"])
            ]
            input_array = np.array(input_features).reshape(1, -1)
            prediction = model.predict(input_array)[0]
            result = "Result: Diabetic" if prediction == 1 else "Result: Not Diabetic"
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("diabetes_predictor.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
