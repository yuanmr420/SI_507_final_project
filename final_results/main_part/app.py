from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import yelp

app = Flask(__name__)

def get_states():
    '''get all states' name from sql database

    Parameters
    ----------
    None


    Returns
    -------
    state_name: list
        A list stored all the U.S. states' name

    '''
    conn = sqlite3.connect('dbv2.db')
    cur = conn.cursor()
    q = f''' SELECT state_name FROM states'''
    state_name = [item[0] for item in cur.execute(q).fetchall()]
    conn.close()
    return state_name

def get_injured_num():
    '''get all states' code and the total number of people died of shooting in 2021 from sql database

    Parameters
    ----------
    None


    Returns
    -------
    state_code: list
        A list stored all the U.S. states' code, like AK, ect
    dead_num:list
        A list stored the total number of people died of shooting in 2021 for each state

    '''
    conn = sqlite3.connect('dbv2.db')
    cur = conn.cursor()
    q = f'''select state_code, dead_num from states'''
    state_code = [item[0] for item in cur.execute(q).fetchall()]
    dead_num = [item[1] for item in cur.execute(q).fetchall()]
    conn.close()
    return state_code, dead_num

def plot():
    '''draw a map plot which depicts how many people were died of shooting in 2021 in each state

    Parameters
    ----------
    None


    Returns
    -------
    div: str
        A map plot which depicts how many people were died of shooting in 2021 in each state

    '''
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
    '''get all cities given the chosen state

    Parameters
    ----------
    state:str
        the name of state


    Returns
    -------
    city_name: list
        all cities name in the given the chosen state
    '''
    conn = sqlite3.connect('dbv2.db')
    cur = conn.cursor()
    q = f'''SELECT City FROM cities WHERE State = "{state}"'''
    city_name = [item[0] for item in cur.execute(q).fetchall()]
    conn.close()
    return city_name

def get_restaurant():
    '''get all 10 restaurant based on yelp api given the chosen city

    Parameters
    ----------
    None


    Returns
    -------
    yelp_list: list
        A list stored 10 Yelp class items
    '''
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
    '''open the homepage

    Parameters
    ----------
    None


    Returns
    -------
    the homepage: homepage.html
        A list stored 10 Yelp class items
    '''
    return render_template('homepage.html')

@app.route('/eating', methods=['POST'])
def eating():
    '''open the eating page

    Parameters
    ----------
    None


    Returns
    -------
    if users choose yes: eating.html
    if users choose no: noteating.html
    '''
    result = request.form['choice1']
    if result == 'Yes':
        return render_template('eating.html')
    else:
        return render_template('noteating.html')

@app.route('/states', methods=['POST'])
def states():
    '''open the states page

    Parameters
    ----------
    None


    Returns
    -------
    if users choose dine-in: states-dine.html
    if users choose deliver: states-deliver.html
    '''
    state_name = get_states()
    div = plot()
    result = request.form['choice2']
    if result == 'dine-in':
        return render_template('states-dine.html', states=state_name, plot_div=div)
    else:
        return render_template('states-deliver.html', states=state_name)

@app.route('/cities', methods=['POST'])
def cities():
    '''open the cities page given the chosen state

    Parameters
    ----------
    None


    Returns
    -------
    the cities page: cities.html
    '''
    state = request.form['choice3']
    cities_name = get_cities(state)
    return render_template('cities.html', cities=cities_name)

@app.route('/restaurants', methods=['POST'])
def restaurants():
    '''open the restaurants page given the chosen city

    Parameters
    ----------
    None


    Returns
    -------
    the restaurants page: restaurants.html
    '''
    restaurants_list = get_restaurant()
    return render_template('restaurants.html', restaurants=restaurants_list)



if __name__ == '__main__':
    app.run(debug=True)