import os
import modal
    
LOCAL=False

if LOCAL == False:
   stub = modal.Stub()
   hopsworks_image = modal.Image.debian_slim().pip_install(["hopsworks==3.0.4","joblib","seaborn","scikit-learn","dataframe-image"])
   @stub.function(image=hopsworks_image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("hopsworks-api-key"))
   def f():
       g()

def g():
    import pandas as pd
    import hopsworks
    import joblib
    import datetime
    from PIL import Image
    from datetime import datetime
    import dataframe_image as dfi
    from sklearn.metrics import confusion_matrix
    from matplotlib import pyplot
    import seaborn as sns
    import requests

    project = hopsworks.login(api_key_value='U6PiDFwDVDQHP26X.XhXDZQ9QKiNwafhLh11PUntcyYW5Zp8aoXhoj1IJTGHDBu8owQJUKbFClHaehyMU')
    fs = project.get_feature_store()
    
    # get model from model registry from hopswork
    mr = project.get_model_registry()
    model = mr.get_model("titanic_modal", version=1)
    model_dir = model.download()
    model = joblib.load(model_dir + "/titanic_model.pkl")
    
    # get batch data from hopsworks feature view
    feature_view = fs.get_feature_view(name="titanic_modal", version=1)
    batch_data = feature_view.get_batch_data()
    
    # make prediciton on whole batch data set
    y_pred = model.predict(batch_data)
    # print(y_pred)
    
    # determine outcome of the latest prediction and download the appropriate image from GitHub
    passenger = y_pred[y_pred.size-1]
    if passenger == 1:
        passenger_str = "survivor"
    else:
        passenger_str = "victim"
    passenger_url = "https://raw.githubusercontent.com/daniel-rdt/serverless_ml_titanic_dr/main/assets/" + passenger_str + ".png"
    
    # print the prediction in console
    if passenger == 1:
        print("Passenger predicted: Survivor!")
    else:
        print("Passenger predicted: Victim!")

    # save image in dataset api
    img = Image.open(requests.get(passenger_url, stream=True).raw)            
    img.save("./latest_passenger.png")
    dataset_api = project.get_dataset_api()    
    dataset_api.upload("./latest_passenger.png", "Resources/images", overwrite=True)
    
    # get feature group and get latest passenger
    titanic_fg = fs.get_feature_group(name="titanic_modal", version=1)
    df = titanic_fg.read()
    # print(df.iloc[-1])

    # determine actual label of passenger and download the appropriate image from GitHub
    label = df.iloc[-1]["survived"]
    if label == 1:
        label_str = "survivor"
    else:
        label_str = "victim"
    label_url = "https://raw.githubusercontent.com/daniel-rdt/serverless_ml_titanic_dr/main/assets/" + label_str + ".png"
    if label == 1:
        print("Passenger actual: Survivor!")
    else:
        print("Passenger actual: Victim!")

    # save the image in dataset api
    img = Image.open(requests.get(label_url, stream=True).raw)            
    img.save("./actual_passenger.png")
    dataset_api.upload("./actual_passenger.png", "Resources/images", overwrite=True)
    
    # get prediction feature group from hopsworks or create new one
    monitor_fg = fs.get_or_create_feature_group(name="titanic_predictions",
                                                version=1,
                                                primary_key=["datetime"],
                                                description="Titanic Passenger Prediction/Outcome Monitoring"
                                                )
    
    # create datetetime information for prediction
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    data = {
        'prediction': [passenger],
        'label': [label],
        'datetime': [now],
       }
    monitor_df = pd.DataFrame(data)
    # insert newest prediction to predictions feature group
    monitor_fg.insert(monitor_df, write_options={"wait_for_job" : False})
    
    history_df = monitor_fg.read()
    # Add our prediction to the history, as the history_df won't have it - 
    # the insertion was done asynchronously, so it will take ~1 min to land on App
    history_df = pd.concat([history_df, monitor_df])


    # get last 5 predictions and store image on dataset api
    df_recent = history_df.tail(5)
    dfi.export(df_recent, './df_recent.png', table_conversion = 'matplotlib')
    dataset_api.upload("./df_recent.png", "Resources/images", overwrite=True)
    
    predictions = history_df[['prediction']]
    labels = history_df[['label']]

    # Only create the confusion matrix when our titanic_predictions feature group has examples of both survivor and victim
    print("Number of different titanic passenger predictions to date: " + str(predictions.value_counts().count()))
    if predictions.value_counts().count() == 2:
        results = confusion_matrix(labels, predictions)
    
        df_cm = pd.DataFrame(results, ['True Victim', 'True Survivor'],
                             ['Pred Victim', 'Pred Survivor'])

        cm = sns.heatmap(df_cm, annot=True)
        fig = cm.get_figure()
        fig.savefig("./confusion_matrix.png")
        # save confusion matrix image to dataset api
        dataset_api.upload("./confusion_matrix.png", "Resources/images", overwrite=True)
    else:
        print("You need 2 different titanic passenger predictions to create the confusion matrix.")
        print("Run the batch inference pipeline more times until you get 2 different titanic passenger predictions") 


if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        stub.deploy("batch_inference_pipeline_daily")
