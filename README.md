# Strong Side Left Side: Streamlit Dashboard
This repo contains the code that runs [our website](https://ssls-airbnb-analysis.streamlit.app/).
- The main (entry) file is "Overview.py"
  - Sub-pages can be found in the "pages" folder
- Relevant information about the raw data, EDA, methodology, and purpose of this project are found on the website's home page.


# Below are instructions about how to run our streamlit dashboard natively (off your local disk)
## To Run for the first time
```
# download files (you can do this via github desktop too)
cd <path to your FIN377 folder> # make sure the cd isn't a repo or inside a repo!
git clone https://github.com/Brooks377/SSLS_dashboard.git

# move the terminal to the new folder
cd SSLS_dashboard

# set up the packages you need for this app to work 
conda env create -f environment.yml
conda activate streamlit-env

# start the app in a browser window
streamlit run Overview.py

# open any IDE you want to modify app - spyder > jupyterlab for this
spyder  # and when you save the file, the app website will update
jupyter lab  # alternative IDE
```
## To Run after first time
```
# In Anaconda Prompt:
cd <path to SSLS_dashboard folder>
conda activate streamlit-env
streamlit run Overview.py
```

[Template Source Repo](https://github.com/donbowen/portfolio-frontier-streamlit-dashboard/)
