# Quick Scan Backend


This project contains the back-end Python Flask application for the Quick Scan project. 
Quick Scan is an application designed to help Capgemini conduct inspections of stores. This application allows for 
conducting a survey that then calculates scores on certain attributes like reachability, customer service, etc.
These scores are then used to generate a document that is readable for the human eye.

This documentation was written with Ubuntu 20.04 as operating system. This means terminal commands and the like assume
that Linux is being used.

This section pertains to the backend server. The backend is an API with database plugged into it. This backend allows us to send and receive data, and store this data. Further on there will be some examples of how this works.

# Technologies used

- Python programming language
- Flask web framework: [docs here](https://flask.palletsprojects.com/en/1.1.x/)
- SQLite database
- There are many Flask plugins integrated into the project.
- The project uses a virtual environment that has to be set up.

# Setup

Before running the project it is important to set up a virtual environment. This obviously requires Python (version 3) to be installed to your device. Please refer to online tutorials on installing Python to your specific operating system. 
The virtual environment is important because it ensures all packages the project needs aren't interfering with your global Python install. This makes it much easier to manage your requirements and the like. 

Important: On many Linux-based operating systems Python version 2 and version 3 have different names. Please run all the commands listed with`python3 commandhere` instead of `python commandhere` on Ubuntu (and check for your specific OS if you aren't sure) to get Python version 3 packages. This is not the case on Windows, as long as you install Python 3 of course.

To set up a virtual environment you do the following:

- First pull the project to your device. You're reading this documentation so you are already on the right Github page.
- run `python –m venv virtual` to create a virtual environment.
- start the virtual environment with `source venv/bin/activate` if it hasn't started yet.
- now install all the relevant packages. The packages the project needs are contained in the `requirements.txt` so you do `pip install -r requirements.txt`.
- At this step you should have all the files and packages that you need setup.

## Running

To run this backend project there's a couple things to keep in mind:

**always run your virtual environment first**: `source venv/bin/activate` Otherwise you will not have the packages needed.

This project was only tested on a local network. You have to start the app with the IP of your device. Please check what your device's local IP is. For example on Windows: Use the commandline to run `ipconfig` then check your local IP.  On Ubuntu there's `ifconfig`, which functions the same way.
 because the app is accessed through Expo/React Native you have to host the application on your public network, the localhost does NOT work.
 
You can configure the IP by starting the application like this:  `flask run --host IPHERE`. Use the IP you got from the instructions earlier.
Example: `flask run --host 192.168.178.11`. This is a local IP. Please make sure it is your local IP because you do not want to run the app on the public internet. (and it likely wouldn't work properly in the first place)

**important (technically frontend but necessary for this to work:** This local IP differs on different devices. The Expo/React Native project is set up to work with the IP in the example>
This works as follows: 

```
apiconfig

import Constants from "expo-constants";

const { manifest } = Constants;

// This is done because the API is currently hosted locally. This grabs the IP from the expo constants.
// I tried connecting to the IP directly, doing various other things, but only this works.

const api = `http://${manifest.debuggerHost.split(':').shift()}:5000`;

export default api;
```

If this does not not work for you try replacing this const with your local IP directly.

# Project structure

Because this is a Python application it is somewhat difficult to separate code into files. I tried my best to do so, but some parts are together because it was way more complicated to configure otherwise.

The project's basic structure is as follows:

- `models`: The folder containing all models for the API. This app uses a typical structure for backends where the database is mapped by models written in code instead of SQL.
- `api.py`: The main API file, this contains all the endpoints and the code that needs to  be executed.
- `app.py`: This is very small but contains the initialization of the Flask app. It allows us to run the app and it allows us to import into all the other files. It also contains the secret key. **This obviously has to be replaced when running in production**
- `quickscan.db`: The database file generated by the app. SQLite doesn't require a configuration or anything like that, it simply generates a file.

This project requires some understanding of how Models work. In this case they were constructed using SQLalchemy. SQLalchemy is an extensive library that allows lots of database interaction, and I recommend reading up on it [here](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) if you want to know more.


