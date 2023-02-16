import os
import modal
from titanic_feature_prep import titanic_prep
    
LOCAL=True

if LOCAL == False:
   stub = modal.Stub()
   image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","seaborn","sklearn","dataframe-image"]) 

   @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("hopsworks-api-key"))
   def f():
       g()

def g():
    import hopsworks
    import pandas as pd

    project = hopsworks.login(api_key_value='U6PiDFwDVDQHP26X.XhXDZQ9QKiNwafhLh11PUntcyYW5Zp8aoXhoj1IJTGHDBu8owQJUKbFClHaehyMU')
    fs = project.get_feature_store()
    # import and prep data by calling prep function
    titanic_df = titanic_prep()

    # create new feature group for prepped titanic dataset and upload titanic_df
    titanic_fg = fs.get_or_create_feature_group(
        name="titanic_modal",
        version=1,
        primary_key=["Pclass","Age","SibSp","Parch","Fare","Sex_female","Sex_male","Embarked_C","Embarked_Q","Embarked_S","Embarked_Unknown"], 
        description="Titanic passenger dataset")
    titanic_fg.insert(titanic_df, write_options={"wait_for_job" : False})

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        with stub.run():
            f()
