import sys
from dataclasses import dataclass

import numpy as numpy
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationFig:
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.DataTransformationFig = DataTransformationFig()

    def get_data_transformer_object(self):
        ''' 
        This function is responsible for data transformation
        
        '''
        try:
            numerical_feature = ["writing_score","reading_score"]
            categorical_feature = ["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
            num_pipeline = Pipeline(
                steps=[
                    ("impute",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequesnt")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler())
                ]
            )

            logging.info("Categorical columns encoding completed")
            logging.info("Numerical columns standard scaling completed")

            preprocessor = ColumnTransformer(
                [
               ("num_pipline",num_pipeline,numerical_feature),
               ("cat_pipeline",cat_pipeline,categorical_feature)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
    

    def initiate_data_tranformtion(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test completed")
            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column = "math_score"
            numerical_column = ["writing_score","reading_score"]

            input_feature_train_df = train_df.drop([target_column],axis=1)
            target_feature_test_df = test_df[target_column]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe.")
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e,sys)