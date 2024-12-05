from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)

# Load the restaurant data from CSV
data_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTLZVWTuFrjIGKtM6bCwo774mvHNSEyzZvNutL0hzSF8ZJsXLq2A-F7BtwhtbT66kvcdcczFuOOC1cB/pub?output=csv"
df = pd.read_csv(data_url)

@app.route('/')
def home():
    return render_template('frontpage.html')

@app.route('/search', methods=['POST'])
def search():
    # Get the form data
    avgcost = request.form.get("avgcost")
    proximity = request.form.get("proximity")
    cuisine = request.form.get("cuisine")
    rest_type = request.form.get("type")
    vegetarian = request.form.get("vegetarian")
    reviews = request.form.get("reviews")

    # Filter data based on the form inputs
    filtered_data = df

    if avgcost:
        filtered_data = filtered_data[filtered_data["avgcost"] == avgcost]

    if proximity:
        proximity = int(proximity)
        filtered_data = filtered_data[filtered_data["proximity"] <= proximity]

    if cuisine:
        filtered_data = filtered_data[filtered_data["cuisine"].str.contains(cuisine, case=False, na=False)]

    if rest_type:
        filtered_data = filtered_data[filtered_data["type"].str.lower() == rest_type.lower()]

    if vegetarian:
        filtered_data = filtered_data[filtered_data["vegetarian"].str.lower() == vegetarian.lower()]

    if reviews:
        reviews = float(reviews)
        filtered_data = filtered_data[filtered_data["reviews"] >= reviews]

    # Check if filtered data is empty
    if filtered_data.empty:
        return "No restaurants found matching your criteria."

    return render_template('results.html', data=filtered_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
