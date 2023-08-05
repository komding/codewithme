import pandas as pd
from flask import Flask, render_template, request
import joblib
import pickle

app = Flask(__name__)

# Load the model
with open("hpp.pkl", "rb") as file:
    model = pickle.load(file)

# Load and prepare the prediction_values.csv
data = pd.read_csv('prediction_values.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input values from the form
        lot_area = float(request.form['lot_area'])
        bedroom_abv_gr = int(request.form['bedroom_abv_gr'])
        garage_cars = int(request.form['garage_cars'])
        duplex = True if request.form['duplex'] == 'True' else False
        overall_qual = int(request.form['overall_qual'])
        fireplaces = int(request.form['fireplaces'])
        pave = True if request.form['pave'] == 'True' else False
        total_bsmt_sf = float(request.form['total_bsmt_sf'])

        # Update the data with user input
        data.loc[0, 'LotArea'] = lot_area
        data.loc[0, 'BedroomAbvGr'] = bedroom_abv_gr
        data.loc[0, 'GarageCars'] = garage_cars
        data.loc[0, 'Duplex'] = duplex
        data.loc[0, 'OverallQual'] = overall_qual
        data.loc[0, 'Fireplaces'] = fireplaces
        data.loc[0, 'Pave'] = pave
        data.loc[0, 'TotalBsmtSF'] = total_bsmt_sf

        # Make a prediction using the updated data
        prediction = model.predict(data)

        return render_template('index.html', prediction=prediction[0])
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
