import folium
import pandas as pd
from flask import Flask,render_template



data = pd.read_csv(r'https://api.covid19india.org/csv/latest/states.csv')

data = data[data['Date']==data.Date.max()]
data = data.sort_values('State')

sl = pd.read_csv('statesGeoInfo.csv')
data = pd.merge(data,sl,on = 'State')

data.set_index(data.State,inplace = True)

cdf = data.nlargest(15, 'Confirmed')[['Confirmed']]




pairs=[(State,confirmed) for State,confirmed in zip(cdf.index,cdf['Confirmed'])]

corona_df = data.copy()
corona_df=corona_df.dropna()

m=folium.Map(location=[20.5937, 78.9629],
##            tiles='Stamen toner',
            zoom_start=4)

def circle_maker(x):
    folium.Circle(location=[x[0],x[1]],
                 radius=float(x[2])/20,
                 color="red",
                 tooltip='confirmed cases:{}'.format(x[2])).add_to(m)
corona_df[['latitude','longitude','Confirmed']].apply(lambda x:circle_maker(x),axis=1)
html_map = m._repr_html_()



app=Flask(__name__)
@app.route('/')
def home():
    return render_template("home.html",table=cdf, cmap=html_map,pairs=pairs)
if __name__=="__main__":
    app.run()
