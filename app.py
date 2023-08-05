'''
import pandas as pd
from flask import Flask, render_template, request
import joblib
import pickle
import xgboost as xgb

app = Flask(__name__)

# Load the model
model = xgb.Booster()
model.load_model("hpp.pkl")

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

        # Convert the data DataFrame to XGBoost DMatrix
        data_dmatrix = xgb.DMatrix(data)

        # Make predictions using the loaded model
        prediction = model.predict(data_dmatrix)


        return render_template('index.html', prediction=prediction[0])
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
'''

import pandas as pd
from flask import Flask, render_template, request
import xgboost as xgb

app = Flask(__name__)

# Load the model
# Load the model
loaded_model = xgb.Booster()
loaded_model.load_model('xgboost_model.model')

# Load and prepare the prediction_values.csv
data = pd.read_csv('prediction_values.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get user input values from the form
            lot_area = float(request.form['lot_area'])
            bedroom_abv_gr = int(request.form['bedroom_abv_gr'])
            garage_cars = int(request.form['garage_cars'])
            duplex = True if request.form['duplex'] == 'True' else False
            overall_qual = int(request.form['overall_qual'])
            fireplaces = int(request.form['fireplaces'])
            pave = True if request.form['pave'] == 'True' else False
            total_bsmt_sf = float(request.form['total_bsmt_sf'])

            # Create a copy of the data to update with user input
            input_data = data.copy()
            input_data.loc[0, 'LotArea'] = lot_area
            input_data.loc[0, 'BedroomAbvGr'] = bedroom_abv_gr
            input_data.loc[0, 'GarageCars'] = garage_cars
            input_data.loc[0, 'Duplex'] = duplex
            input_data.loc[0, 'OverallQual'] = overall_qual
            input_data.loc[0, 'Fireplaces'] = fireplaces
            input_data.loc[0, 'Pave'] = pave
            input_data.loc[0, 'TotalBsmtSF'] = total_bsmt_sf

            # Convert input data to XGBoost DMatrix
            input_dmatrix = xgb.DMatrix(input_data)

            # Make predictions using the loaded model
            prediction = loaded_model.predict(input_dmatrix)

            return render_template('index.html', prediction=prediction[0])
        except Exception as e:
            print("Error:", e)
            return render_template('index.html', prediction="Error occurred")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
