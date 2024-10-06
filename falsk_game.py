from flask import Flask, render_template, request, jsonify, abort
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import random
import os

app = Flask(__name__)

# Planet information
planet_info = {
    "Mercury": {"gravity": 3.7, "color": "#808080", "game_gravity": 0.50},
    "Venus": {"gravity": 8.87, "color": "#FFC649", "game_gravity": 0.704},
    "Earth": {"gravity": 9.81, "color": "#00FF00", "game_gravity": 0.8},
    "Mars": {"gravity": 3.721, "color": "#FF0000", "game_gravity": 0.58},
    "Jupiter": {"gravity": 24.79, "color": "#FF8C00", "game_gravity": 2.328},
    "Saturn": {"gravity": 10.44, "color": "#EEE8AA", "game_gravity": 0.89},
    "Uranus": {"gravity": 8.69, "color": "#ADD8E6", "game_gravity": 0.668},
    "Neptune": {"gravity": 11.15, "color": "#0000FF", "game_gravity": 1.137}
}

def create_gravity_chart():
    gravity_data = pd.DataFrame.from_dict(planet_info, orient='index')
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(gravity_data.index, gravity_data['gravity'], color=gravity_data['color'])
    ax.set_ylabel("Gravity (m/s²)")
    ax.set_title("Gravity on Different Planets")
    plt.xticks(rotation=45)
    
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route('/')
def home():
    try:
        chart_image = create_gravity_chart()
        return render_template('index.html', planets=planet_info.keys(), chart_image=chart_image)
    except Exception as e:
        app.logger.error(f"Error rendering template: {str(e)}")
        app.logger.error(f"Current working directory: {os.getcwd()}")
        app.logger.error(f"Template folder path: {app.template_folder}")
        app.logger.error(f"Files in template folder: {os.listdir(app.template_folder)}")
        return f"An error occurred: {str(e)}", 500

@app.route('/planet_info', methods=['POST'])
def get_planet_info():
    planet = request.form['planet']
    weight = float(request.form['weight'])
    info = planet_info[planet]
    return jsonify({
        'actual_gravity': info['gravity'],
        'game_gravity': info['game_gravity'],
        'earth_weight': weight,
        'planet_weight': weight * info['gravity'] / 9.81
    })

@app.route('/collect_coins', methods=['POST'])
def collect_coins():
    planet = request.form['planet']
    gravity = planet_info[planet]['game_gravity']
    coins_collected = random.randint(1, 10)
    score = coins_collected * int(10 / gravity)
    return jsonify({
        'coins_collected': coins_collected,
        'score': score,
        'message': f"The {'lower' if gravity < 1 else 'higher'} gravity on {planet} {'made it easier' if gravity < 1 else 'made it harder'} to collect coins!"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
