# Strong Side Left Side: Streamlit Dashboard
This repo contains the code that runs [our website](https://ssls-airbnb-analysis.streamlit.app/).
- The main (entry) file is "Overview.py"
  - Sub-pages can be found in the "pages" folder
- Relevant information about the raw data, EDA, methodology, and purpose of this project are found on the website's home page.

## Below are instructions about how to run our streamlit dashboard natively (off your local disk)
### To Run for the first time
```
# download files (you can do this via github desktop too)
cd <path to your preferred folder> # don't put a repo inside a repo!
git clone https://github.com/BrooksWalsh/SSLS_dashboard.git

# move the terminal to the new folder
cd SSLS_dashboard

# set up the packages you need for this app to work 
conda env create -f env-config.yml

# activate the environment created by env-config.yml
conda activate ssls-env

# start the app in a browser window
streamlit run Overview.py
```

### To Run after first time
```
# In Anaconda Prompt:
cd <path to SSLS_dashboard folder>
conda activate streamlit-env
streamlit run Overview.py
```

### Making Modifications
- You can modify the app while it's running locally using your preferred IDE/editor
- Saving changes to the ```<app/page>.py``` files will update the local app automatically
- Pushing changes to github will update the online app hosted by streamlit (may need to reboot app)


### If you need to remove a conda environment
```conda remove --name <env_name> --all```


[Template Source Repo](https://github.com/donbowen/portfolio-frontier-streamlit-dashboard/)
