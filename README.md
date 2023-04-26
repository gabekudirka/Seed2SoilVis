### Installation and Setup
The application is currently hosted with sample data at: https://gracious-heisenberg-a8a687.netlify.app/

To run this application with the uploaded sample data please use Node v14 and run the following commands
```
npm install
npm run serve
```

To run this application with new data:
1. Add vehicle and trip data to raw_data or another specified folder within data_processing
2. Update filepath and filename for input and output files in 'preprocess_trip_data.py' and run
```
python preprocess_trip_data.py
```
3. Update filepath and filename for input and output files in 'format_app_data.py' and run
```
python format_app_data.py
```
4. Four files should be created in the specified output directory: depts.json, fleet.json, trips.json, and 'heatmap_overlay.json'. Place these files in src/data
5. Run the following commands to start the application
```
npm install
npm run serve
```

### Code Overview
There are two primary folders for this application, src and data_processing. The code for processing raw data from GeoTab is in data_processing and is written in Python. src contains all code to run the application and is written in JavaScript and HTML using the Vue.js framework.

/data_processing
    preprocess_trip_data.py: This file preprocesses data for trips using python. It formats some of the columns for consistency and uses a geocoder to convert named locations in the data to latitude and longitude coordinates.
    format_app_data.py: This file should be run after preprocess_trip_data.py and extracts necessary data about vehicles, departments, and vehicle trips and exports them to json files which are readable by the application.

All of the code in the node_modules folder comes from external libraries/packages

The src folder contains all of the code that I have written for the application. Within this folder the large majority of code lies within the components folder, where each file defines a specific component of the application. The data folder contains the processed data and the store folder contains the index.js file which is used to house the state variables and the functions which mutate state variables. Lastly, the App.vue file is the central component of the application and is where all other components are initialized from.


 