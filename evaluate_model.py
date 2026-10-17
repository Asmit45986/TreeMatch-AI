import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

# 1. Load trained soil classification CNN model
model_path = r"D:\project data\AI_afforestation\models\soil_classifier.h5"  # Apne model file ka path update karein
model = tf.keras.models.load_model(model_path)

# 2. Test dataset directory define karein
test_dir = r"D:\project data\AI_afforestation\data\test"  # Test dataset folder path

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

# 3. Model Predictions calculate karein
predictions = model.predict(test_generator)
y_pred = np.argmax(predictions, axis=1)
y_true = test_generator.classes
class_labels = list(test_generator.class_indices.keys())

# 4. Display Metrics
print("\n================ Classification Report ================\n")
print(classification_report(y_true, y_pred, target_names=class_labels))

print("\n================ Confusion Matrix ================\n")
cm = confusion_matrix(y_true, y_pred)
print(cm)