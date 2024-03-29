# Anime-Genre-Classification

A text classification model from data collection, model training, and deployment. <br/>
The model can classify 50 different types of anime genres <br/>The keys of `Deployment\genre_types_encoded.json` shows the anime genres

 ## Data Collection

Data was collected from a Anime Website Listing: https://myanimelist.net/topanime.php <br/>The data collection process is divided into 2 steps:

1. **Anime URL Scraping:** The anime urls were scraped with `anime_url_scraper.py` and the urls are stored along with anime title in `Data\anime_urls.csv`
2. **Anime Details Scraping:** Using the urls, anime description and genres are scraped with `anime_genre_scraper.py` and they are stored in `Data\anime_genre_details_merged.csv`

In total, I scraped 8950 anime details

## Data Preprocessing

Initially there were *74* different genres in the dataset. After some analysis, I found out *50* of them are rare (probably custom genres by users). So, I removed those genres and then I have *50* genres. After that, I removed the description without any genres resulting in *8927* samples.

## Model Training

Finetuned a `distilrobera-base` model from HuggingFace Transformers using Fastai and Blurr. The model training notebook can be viewed [here](https://github.com/mynul-islam-madhurjo/Anime-Genre-Classification/blob/main/Notebooks/anime_multilabel_text_classification.ipynb) 

## Model Compression and ONNX Inference

The trained model has a memory of 300+MB. I compressed this model using ONNX quantization and brought it under 80MB. 

## Model Deployment

The compressed model is deployed to HuggingFace Spaces Gradio App. The implementation can be found in `deployment` folder or [here](https://huggingface.co/spaces/mynul-islam-madhurjo/Anime-Genre-Classifier)

<img src = "Deployment/gradio_app.png" width="800" height="400">

## Web Deployment
Deployed a Flask App built to take description and show the genres as output. Check `live ` branch. The website is live [here](https://anime-genre-classification.onrender.com) 

<img src = "Deployment/flask_app_home.png" width="800" height="400">
<img src = "Deployment/flask_app_results.png" width="800" height="600">

