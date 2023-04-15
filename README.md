# portfolio-frontier-streamlit-dashboard
 Fork of streamlit project for a template
 - fix for error message about pylsp when using spyder 
   - ```conda install -c conda-forge python-lsp-server ```
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
streamlit run app.py

# open any IDE you want to modify app - spyder > jupyterlab for this
spyder  # and when you save the file, the app website will update
jupyter lab  # alternative IDE
```
## To Run after first time
```
####
# my current path: C:\Users\dbawa\ZZ__School_Related\FIN_377\SSLS_dashboard
####

# In Anaconda Prompt:
cd <path to SSLS_dashboard folder>
streamlit run app.py
```

[Template Source Repo](https://github.com/donbowen/portfolio-frontier-streamlit-dashboard/)
