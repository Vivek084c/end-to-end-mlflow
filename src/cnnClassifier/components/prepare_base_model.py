import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from pathlib import Path
from src.cnnClassifier.config.configuration import PrepareBaseModelConfig


class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    def get_base_model(self):
        """
        To download the base model with config as defined in __init__
        """
        self.model = tf.keras.applications.vgg16.VGG16(
        input_shape = self.config.params_image_size,
        weights = self.config.params_weight,
        include_top = self.config.params_include_top
        )

        self.save_model(path=self.config.base_model_path, model=self.model)

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        """
        static function to save the model
        Args: 
            model(tf.keras.Model): model to be saved
        """
        model.save(path)

    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate):
        """
        modify the base model and save it with the desired parameter
        Args:
            model(tf.keras.Model): base model 
            classes : no of classes 
            freeze_all: base model parameter
            freeze_till: base model parameter
            learning_rate: Model learning rate
        Returns:
            full_model: model after altering the base model
        """
        #freezing the layers for desired depth
        if freeze_all:
            for layer in model.layers:
                model.trainable = False
        elif (freeze_till is not None) and (freeze_till>0):
            for layer in model.layers[:-freeze_till]:
                model.trainable = False

        flatter_in = tf.keras.layers.Flatten()(model.output)
        prediction = tf.keras.layers.Dense(
            units=classes,
            activation="softmax"
        )(flatter_in)

        full_model = tf.keras.models.Model(
            inputs = model.input,
            outputs = prediction
        )

        full_model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate), 
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )

        full_model.summary()
        return full_model
    
    def update_base_model(self):
        """
        save the modified base model version
        """
        self.full_model = self._prepare_full_model(
            model = self.model,
            classes=self.config.params_classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config.params_learning_rate
        )

        self.save_model(path=self.config.update_base_model_path, model=self.full_model)
            
