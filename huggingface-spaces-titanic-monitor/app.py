import gradio as gr
from PIL import Image
import hopsworks

project = hopsworks.login(api_key_value='U6PiDFwDVDQHP26X.XhXDZQ9QKiNwafhLh11PUntcyYW5Zp8aoXhoj1IJTGHDBu8owQJUKbFClHaehyMU')
fs = project.get_feature_store()

dataset_api = project.get_dataset_api()

dataset_api.download("Resources/images/latest_passenger.png", overwrite=True)
dataset_api.download("Resources/images/actual_passenger.png", overwrite=True)
dataset_api.download("Resources/images/df_recent.png", overwrite=True)
dataset_api.download("Resources/images/confusion_matrix.png", overwrite=True)

with gr.Blocks() as demo:
    with gr.Row():
      with gr.Column():
          gr.Label("Today's Predicted Image")
          input_img = gr.Image("latest_passenger.png", elem_id="predicted-img")
      with gr.Column():          
          gr.Label("Today's Actual Image")
          input_img = gr.Image("actual_passenger.png", elem_id="actual-img")        
    with gr.Row():
      with gr.Column():
          gr.Label("Recent Prediction History")
          input_img = gr.Image("df_recent.png", elem_id="recent-predictions")
      with gr.Column():          
          gr.Label("Confusion Maxtrix with Historical Prediction Performance")
          input_img = gr.Image("confusion_matrix.png", elem_id="confusion-matrix")        

demo.launch()
