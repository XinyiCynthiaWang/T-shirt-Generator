import random
import picture
import combination

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from time import time

from prediction import predict


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tshirt.db'


db = SQLAlchemy(app)

class Tshirt(db.Model):
    userId = db.Column(db.Integer, primary_key=True) 
    isRealistic= db.Column(db.Boolean, nullable=False, default=False)
    hasSlogan = db.Column(db.Boolean, nullable=False, default=False)
    isColourful = db.Column(db.Boolean, nullable=False, default=False)
    sloganTopic = db.Column(db.String(200), default="")

    def __repr__(self):
        return '<T-shirt %r>' % self.userId

new_tshirt = Tshirt(userId = random.randint(1000, 9999))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            if request.form['customize'] in ['realistic', 'nonrealistic'] :
                new_tshirt.isRealistic = True if request.form['customize'] == 'realistic' else False
                return render_template('index.html', step=2, slogan=False) 
            elif request.form['customize'] in ['slogan', 'noslogan']:
                new_tshirt.hasSlogan = True if request.form['customize'] == 'slogan' else False
                if new_tshirt.hasSlogan:
                    return render_template('index.html', step=2, slogan = True) 
                else:
                    return render_template('index.html', step=3) 
            elif request.form['customize'] in ['blacknwhite', 'colourful']:
                new_tshirt.isColourful = True if request.form['customize'] == 'colourful' else False
                print(new_tshirt.userId, new_tshirt.isColourful, new_tshirt.hasSlogan, new_tshirt.isRealistic, new_tshirt.sloganTopic)
                db.session.add(new_tshirt)
                db.session.commit()
                return redirect(url_for('generate', id = new_tshirt.userId))
        except:
            new_tshirt.sloganTopic = request.form['slogan']
            return render_template('index.html', step=3)
    else:
        return render_template('index.html', step=1)

@app.route('/generator/<int:id>')
def generate(id):
    tshirt_to_generate = Tshirt.query.get_or_404(id) 

    start_time_feature = time()

    feature_collection = combination.combination(tshirt_to_generate)

    passed_time_feature = time() - start_time_feature
    print(f"Feature Preparation Running Time: {passed_time_feature}")

    feature_collection_without_text = feature_collection.drop(['text'], axis = 1)
    start_time_model = time()

    feature_collection_without_text = feature_collection_without_text.astype(int)
    best_combination = predict(feature_collection_without_text)

    passed_time_model = time() - start_time_model
    print(f"Model Fitting Running Time: {passed_time_model}")

    start_time_design = time()

    completed_tshirt = picture.make_tshirt(tshirt_to_generate.userId, feature_collection.loc[best_combination])
    passed_time_design = time() - start_time_design
    print(f"Design Generationg Running Time: {passed_time_design}")

    tshirt_name = completed_tshirt.split('/')[-1]
    return render_template('index.html', generated=True, file_name = tshirt_name)
        
if __name__ == "__main__":
    
    app.run(debug = True)
