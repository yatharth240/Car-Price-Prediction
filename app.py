from flask import Flask,render_template,request
import pandas as pd
from pycaret.regression import load_model,predict_model
from datetime import datetime

app = Flask(__name__)

model = load_model('model')


@app.route("/",methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/results",methods=['GET','POST'])
def results():

    if request.method == "POST":
        try: 
            brand_name = request.form.get('brand')
            year_of_the_model = request.form.get('year')
            kms = request.form.get('kms')
            views = request.form.get('views')
            photos = request.form.get('photos')
            var = request.form.get('variant')
            trans = request.form.get('Transmission')
            data = pd.DataFrame.from_dict({
            'Brand Name' : [brand_name,],
            'Kms Driven' : [int(kms),],
            'Variant' : [var,],
            'Transmission Type' : [trans,],
            'Number of Photos Uploaded' : [int(photos),],
            'Total Views' : [int(views)],
            'Total Years Passed' : [datetime.now().year - int(year_of_the_model)]

        })
            ans = predict_model(model, data = data)
            price = ans['Label'][0]
        
            return render_template('results.html',content={
                'price' : price
            })
        except:
            return "There was some error !! "

    
    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug= True,threaded = True)