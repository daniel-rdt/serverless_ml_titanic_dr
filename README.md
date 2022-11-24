# Scalable Machine Learning and Deep Learning - Lab1: Titanic Dataset Classifier

#  Github repository:
https://github.com/daniel-rdt/serverless_ml_titanic_dr

# File running sequence for titanic survival prediction:
1. run: python titanic-feature-pipeline.py (once)
2. run: python titanic-training-pipeline.py (once)
3. upload huggingface-spaces-titanic folder files to HuggingFace

Hugging Face Spaces public URL: https://huggingface.co/spaces/daniel-rdt/titanic

# File running sequence for titanic survival prediction for most recent passenger added:
4. run: python titanic-feature-pipeline-daily.py (set LOCAL=FALSE to start scheduled daily run on MODAL)
5. run: python titanic-batch-inference-pipeline.py (set LOCAL=FALSE to start scheduled daily run on MODAL) 
6. upload huggingface-spaces-titanic-monitor folder files to HuggingFace

Hugging Face Spaces public URL: https://huggingface.co/spaces/daniel-rdt/titanic_monitor

# File explanation:
titanic_feature_prep.py:
- contains the function "titanic_prep()"
- downloading data from GitHub repository;
- feature engineering: 
- 1. removed "PassengerId","Name","Ticket" and "Cabin" columns;
- 2. all ages rounded up to next integer, so age less than 1 is rounded up to 1;
- 3. filled missing values for "Age" with created random age values in range from min. age to max. age;
- 4. filled missing values for "Embarked" with new "Unknown" category;
- 5. turned categorical variables ("Embarked" and "Sex") into binary numerical variables;
- 6. dropped old categorical columns "Sex" and "Embarked";
- returns a clean, prepped titanic dataset;

titanic-feature-pipeline.py:
- can be run either locally or with MODAL;
- applies titanic_prep function to yield the prepped titanic data set as titanic_df;
- creates Hopsworks feature group and stores features and labels of titanic_df into Hopsworks;

titanic-training-pipeline.py:
- can be run either locally or with MODAL;
- loades features and labels from Hopsworks feature store either as feature view or creates feature view from existing feature group;
- Train-Test-Split with 80/20;
- runs K-nearest-neighbours algorithm on train split;
- runs evaluation on test split and visualized as confusion matrix;
- Uploads model to the Hopsworks Model Registry;

huggingface-spaces-titanic folder:
- folder containing main app for user interface and requirements;
- app let's the user input feature values and returns a prediction

titanic-feature-pipeline-daily.py:
- same as titanic-feature-pipeline-daily when BACKFILL=TRUE;
- when BACKFILL=FALSE: generates new random passenger (either survivor or victim) and adds to Hopsworks feature group;
- ranges for survivor/victim features were determined according to min/max values or existing categories of a feature from the original titanic data set filtered for the labels respectively;

titanic-batch-inference-pipeline.py:
- can be run either locally or with MODAL on a daily schedule;
- gets model from Hopsworks registry and batch data from feature view;
- predicts if the synthetic passengers survived or not;
- downloads appropriate images for prediction and creates up to date confusion matrix when there have been 2 predictions made to date;
- stores predictions to Hopsworks;


huggingface-spaces-titanic-monitor folder:
- folder containing main app for user interface and requirements;
- app shows the most recent synthetic passenger prediction and real label, and a confusion matrix with historical prediction performance; 

# General notes
- everyone aged less than 1 year old is considered as 1 year old person;
- randomly generated passengers ranges for victims and survivors are very similar which may result in very ambiguous prediction results