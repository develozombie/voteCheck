from flask import Flask, render_template, jsonify
import boto3
from boto3.dynamodb.conditions import Key
from operator import itemgetter

app = Flask(__name__)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tStand')  # Using the existing table name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    # Scan the table and get all items
    response = table.scan(
        ProjectionExpression='Nombre, Voto'
    )
    items = response['Items']
    
    # Convert None or empty Voto to 0 for sorting
    for item in items:
        if 'Voto' not in item or item['Voto'] is None or item['Voto'] == '':
            item['Voto'] = '0'
    
    # Filter out items with Voto = 0, then sort by number of votes in descending order
    filtered_items = [item for item in items if int(item['Voto']) > 0]
    sorted_items = sorted(filtered_items, key=lambda x: int(x['Voto']), reverse=True)
    
    # Get top 10 items
    top_10 = sorted_items[:10]
    
    return {'items': top_10}

if __name__ == '__main__':
    app.run(debug=True)
