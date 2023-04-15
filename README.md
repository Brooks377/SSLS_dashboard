# portfolio-frontier-streamlit-dashboard
 Fork of streamlit project for a template
 - fix for error message about pylsp when using spyder 
   - ```conda install -c conda-forge python-lsp-server ```
## To Run for the first time
```
# download files (you can do this via github desktop too)
cd <path to your FIN377 folder> # make sure the cd isn't a repo or inside a repo!
git clone https://github.com/Brooks377/SSLS_dashboard.git

# move the terminal to the new folder (adjust next line if necessary)
cd portfolio-frontier-streamlit-dashboard  

# this deletes the .git subfolder, so you can make this your own repo
# MAKE SURE THE cd IS THE portfolio-frontier-streamlit-dashboard FOLDER FIRST!
rm -r -fo .git 

# set up the packages you need for this app to work 
# (YOU CAN SKIP THESE if you have already streamlit-env, or you can 
# give this one a slightly diff name by modifying the environment.yml file)
conda env create -f environment.yml
conda activate streamlit-env

# start the app in a browser window
streamlit run app.py

# open any IDE you want to modify app - spyder > jupyterlab for this
spyder  # and when you save the file, the app website will update
```
## To Run after first time
```
####
# my current path: C:\Users\dbawa\ZZ__School_Related\FIN_377\SSLS_dashboard
####

# In Anaconda Prompt
cd <path to SSLS_dashboard folder>
streamlit run app.py
```

[Template Source Repo](https://github.com/donbowen/portfolio-frontier-streamlit-dashboard/)
