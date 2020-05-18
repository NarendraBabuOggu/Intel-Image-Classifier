# Starter for deploying [fast.ai](https://www.fast.ai) models on [Google App Engine](https://cloud.google.com/appengine)
This repo can be used as a starting point to deploy Fast.AI or Pytorch Models on Google App Engine.

This is based on the deployment tutorial by FastAI at https://course.fast.ai/deployment_google_app_engine.html # Test it out with bear images!

You can test your changes locally by installing Docker and using the following command:

```
docker build -t fastai-v3 . && docker run --rm -it -p 5000:5000 fastai-v3
```

or By creating a Virtual Environment with the requirements and test with following Command

"""
python app/server.py server

"""

The notebook Explains the training of the Classifier model on Intel Image Dataset.


To use this repo to deploy your custom model Please update the following

Requirements.txt - to include your custom model requirements

Inside app/server.py - update classes to your custom model classes and classifier path to ur custom model's google drive path(direct download link)