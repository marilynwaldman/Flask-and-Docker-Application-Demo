import requests
from flask import Flask, jsonify
import tarfile
import os as os
import urllib3
import shutil
from pathlib import Path
import geopandas as gpd
#import folium as fl
#from folium.plugins import FastMarkerCluster,MarkerCluster,MiniMap
#import branca.colormap as cm

app = Flask(__name__)

api_url = "https://raw.githubusercontent.com/HarunMbaabu/Flask-and-Docker-Application-Domo/main/students.json"
url='https://tgftp.nws.noaa.gov/SL.us008001/DF.sha/DC.cap/DS.WWA/current_all.tar.gz'
@app.route("/doggy")
def get_json_data():
    cwd = Path.cwd()
    
    dest_path = os.path.join(os.getcwd(), 'downloads/')
     
    if os.path.exists(dest_path) and os.path.isdir(dest_path):
         shutil.rmtree(dest_path)

    os.mkdir(dest_path) 
    destination =  str(dest_path)+'current_all.tar.gz'

    http = urllib3.PoolManager()
    try:
         resp = http.request(
             "GET",
              url,
              preload_content=False)
         with open(destination,"wb") as f:
             for chunk in resp.stream(32):
                f.write(chunk)

         resp.release_conn()  
         wxdata = tarfile.open(name=destination)
         wxdata.list(verbose=True)
         wxdata.extractall(path=str(dest_path)+'/current_all/')
         infile = str(dest_path) + '/current_all/current_all.shp'
         if os.path.exists(infile):
              weather_df = gpd.read_file(infile)    
              weather_df = weather_df.drop(columns=['PHENOM','SIG','WFO','EVENT','ONSET','ENDS','CAP_ID','MSG_TYPE','VTEC'])  
         #mbr = fl.Map(location=[40.0,-95.0],zoom_start=4,tiles="Stamen Toner")

         #colormap = cm.linear.Set1_09.scale(0,10)
         return infile
    except Exception as e:
      print("Error occured :: %s" % e.message)

  

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0" ,port=8000)      
