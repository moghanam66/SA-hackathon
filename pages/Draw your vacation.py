import streamlit as st
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from bardapi import Bard
from annoy import AnnoyIndex
import os
from PIL import Image
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('attractionsEng.csv')
bardtoken='WwiytssR_Lr_Ddif1Gl4z4wdC6AwDgKAvaDoe5XcnB9Yl7_2DGw6FjDiUkQ7EZ-PiogeQQ.'
# Load the MobileNetV2 model from TensorFlow Hub
model_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4"
model = tf.keras.Sequential([hub.KerasLayer(model_url, input_shape=(224, 224, 3))])

# Function to load and preprocess images
@st.cache_data
def load_and_preprocess_image(_image):
    img = _image.resize((224, 224))
    img = img.convert("RGB")  # Convert image to RGB if it has an alpha channel
    img = np.array(img) / 255.0  # Normalize image pixels to [0, 1]
    return img

@st.cache_resource
def loadImages():
    # Load dataset images and extract features
    image_folder = 'csv_images'
    image_files = os.listdir(image_folder)

    image_features = []
    for image_file in image_files:
        img = Image.open(os.path.join(image_folder, image_file))
        img = load_and_preprocess_image(img)
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        features = model.predict(img)
        image_features.append(features.squeeze())

    # Build Annoy index
    annoy_index = AnnoyIndex(1280, "euclidean")
    for i, feature in enumerate(image_features):
        annoy_index.add_item(i, feature)
    annoy_index.build(10)
    return annoy_index,image_files,image_folder
annoy_index,image_files,image_folder=loadImages()

st.title("Image Similarity Search")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg",'png'])

if uploaded_file is not None:
    user_img = Image.open(uploaded_file)
    st.image(user_img, caption="Uploaded Image", use_column_width=True)

    user_img = load_and_preprocess_image(user_img)
    user_features = model.predict(np.expand_dims(user_img, axis=0))

    # Find the most similar image in the dataset
    n_nearest_neighbors = 1
    nearest_indices = annoy_index.get_nns_by_vector(user_features.squeeze(), n_nearest_neighbors)
    nearest_image_file = image_files[nearest_indices[0]]

    similar_image = Image.open(os.path.join(image_folder, nearest_image_file))
    col11,col12=st.columns([0.5,0.5])
    with col11:
        site=df[df.index==int(nearest_image_file.replace('.jpg',''))]['attractionSite'].values[0]
        latitude=df[df.index==int(nearest_image_file.replace('.jpg',''))]['Latitude'].values[0]
        longitude=df[df.index==int(nearest_image_file.replace('.jpg',''))]['Longitude'].values[0]

        new_row = {"Place": site, "Latitude":latitude, "Longitude":longitude}
        cities = pd.DataFrame([new_row])

        # Create the Plotly figure
        fig = px.scatter_mapbox(cities, lat="Latitude", lon="Longitude", hover_name="Place",
                                color_discrete_sequence=["fuchsia"], zoom=10,size=[10])
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        st.plotly_chart(fig)
    with col12:
        st.image(similar_image, caption="Similar Image", use_column_width=True)
    index_without_extension = int(nearest_image_file.split('.')[0])

    row = df.loc[index_without_extension]
    # Create a sentence from column values (touristic places)
    sentence = f"The place : **{row['attractionSite']}**"
    bard = Bard(token=bardtoken)
    
    st.title(sentence)
    answer=bard.get_answer(f"Hi")['content']
    delimeters=re.findall(r"\[.*\]",answer)
    
    for deli in delimeters:
            answer=answer.replace(deli,'')
    st.markdown(answer)
