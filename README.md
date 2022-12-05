To run this application please use Node v14 and run the following commands
```
npm install
npm run serve
```

The website where this application is: https://gracious-heisenberg-a8a687.netlify.app/

I could not embed the video into my application due to the nature of my project, here is a link to the screen-cast on YouTube: https://youtu.be/X5AcbTxgdnU

The process book for this project is located in the repo and is titled ProcessBook.pdf


### Code Overview
All of the code for initial data processing is located in the data_processing folder. The primary three files used to process the data are process_fleet.ipynb, process_trips.ipynb, and combine_data.ipynb

All of the code in the node_modules folder comes from external libraries/packages

The src folder contains all of the code that I have written for the application. Within this folder the large majority of code lies within the components folder, where each file defines a specific component of the application. The data folder contains the processed data and the store folder contains the index.js file which is used to house the state variables and the functions which mutate state variables. Lastly, the App.vue file is the central component of the application and is where all other components are initialized from.


