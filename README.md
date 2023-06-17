# Travelogue
### The idea is an AI web application to support Tourism in Saudi Arabia by helping them know more about Touristic places by:
##### Through the main page : (Home.py) controling all project's scripts which are :
- **AI chatbot** (pages/1-Plan your vacation .py) : using openAI through langChain using vector stores of Scrapped dataset serves our business needs. - Interactive FAQs about Tourism in Saudi Arabia.
- **Image recommender** (pages/2-Search by image.py): user can upload any image for any place and the model would retrieve the most Saudi touristic place similar to this place and text generated out of the scrapped text about this place.
- **Travel Planner** (pages/3-Ask me.py): user can write anything he needs and use Google Bard API for creating a plan for the tourist supported by more information about each place in this plan.

**Note** : All services Supports (English and Arabic) Languages.

![Project Flow](project-Flow.png)

### Technologies Used :
- LangChain
- openAI
- Streamlit
- Deep_Translator
- Transformers
- Annoy
- Tensorflow
- Faiss-cpu
