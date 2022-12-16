from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import yelp

app = Flask(__name__)

def get_states():
    conn = sqlite3.connect('dbv2.db')
    cur = conn.cursor()
    q = f''' SELECT state_name FROM states'''
    state_name = [item[0] for item in cur.execute(q).fetchall()]
    conn.close()
    return state_name

def get_injured_num():
    conn = sqlite3.connect('dbv2.db')
    cur = conn.cursor()
    q = f'''select state_code, dead_num from states'''
    state_code = [item[0] for item in cur.execute(q).fetchall()]
    dead_num = [item[1] for item in cur.execute(q).fetchall()]
    conn.close()
    return state_code, dead_num

def plot():
    state_code, dead_num = get_injured_num()
    df = pd.DataFrame({'codes':state_code, 'dead_num':dead_num})
    fig = go.Figure(data=go.Choropleth(
        locations=df['codes'],
        z=df['dead_num'].astype(float),
        locationmode='USA-states',
        hovertext=df['codes'],
        colorscale='Reds',
        colorbar_title='the Total Number of  People Died of Shooting in 2021'
    ))
    fig.update_layout(geo_scope='usa')
    div = fig.to_html(full_html=False)
    return div

def get_cities(state):
    conn = sqlite3.connect('dbv2.db')
    cur = conn.cursor()
    q = f'''SELECT City FROM cities WHERE State = "{state}"'''
    city_name = [item[0] for item in cur.execute(q).fetchall()]
    conn.close()
    return city_name

def get_restaurant():
    city = request.form['choice4']
    params = {'location':city,'limit':10,'term':'dinner'}
    host = yelp.API_HOST
    base_url = yelp.SEARCH_PATH
    key = yelp.API_KEY
    CACHE_DICT = yelp.open_cache()
    results = yelp.request_with_cache(host, base_url, key, params,CACHE_DICT)
    yelp_list = [yelp.Yelp(restaurant) for restaurant in results['businesses']]
    return yelp_list

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/eating', methods=['POST'])
def eating():
    result = request.form['choice1']
    if result == 'Yes':
        return render_template('eating.html')
    else:
        return render_template('noteating.html')

@app.route('/states', methods=['POST'])
def states():
    state_name = get_states()
    div = plot()
    result = request.form['choice2']
    if result == 'dine-in':
        return render_template('states-dine.html', states=state_name, plot_div=div)
    else:
        return render_template('states-deliver.html', states=state_name)

@app.route('/cities', methods=['POST'])
def cities():
    state = request.form['choice3']
    cities_name = get_cities(state)
    return render_template('cities.html', cities=cities_name)

@app.route('/restaurants', methods=['POST'])
def restaurants():
    restaurants_list = get_restaurant()
    return render_template('restaurants.html', restaurants=restaurants_list)



if __name__ == '__main__':
    app.run(debug=True)