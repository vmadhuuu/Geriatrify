from flask import Flask, render_template, url_for, flash, redirect
import joblib
from flask import request
import numpy as np

app = Flask(__name__, template_folder='templates')


@app.route("/")
@app.route("/Heart")
def cancer():
    return render_template("heart.html")


def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if(size == 7):
        loaded_model = joblib.load(
            r'E:\External Projects\MajorProject\model_api\Heart_API\heart_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/predict', methods=["POST"])
def predict():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        # diabetes
        if(len(to_predict_list) == 7):
            result = ValuePredictor(to_predict_list, 7)

    if(int(result) == 1):
        prediction = "I understand that this news is difficult to hear, but you have been diagnosed positive. Kindly consult your doctor to know further about the details. Quick remedy can be taken from the recommendations below!"
        return(render_template("recommend.html", prediction_text=prediction))

    else:
        prediction = "Congratulations on your recovery! Please continue to take care of yourself to maintain your health."
        return(render_template("result.html", prediction_text=prediction))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
