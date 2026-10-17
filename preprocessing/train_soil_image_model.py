import os
import tensorflow as tf
import cv2
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models, Sequential
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

print("🚀 Starting Soil Classifier Training...")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOIL_DATASET_DIR = os.path.join(BASE_DIR, "datasets", "SoilDataset")
CHECKPOINTS_DIR = os.path.join(BASE_DIR, "checkpoints")

os.makedirs(CHECKPOINTS_DIR, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
NUM_CLASSES = 7

# 1. Thorough Corrupt File Removal with OpenCV & TF Decode Test
print("🧹 Thoroughly scanning and cleaning corrupted images from SoilDataset...")
removed_count = 0

for root, dirs, files in os.walk(SOIL_DATASET_DIR):
    for file in files:
        file_path = os.path.join(root, file)
        
        # Non-image / hidden files filter
        if file.startswith('.') or not file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            try:
                os.remove(file_path)
                removed_count += 1
            except Exception:
                pass
            continue

        # Test 1: Try reading via OpenCV
        img_cv = cv2.imread(file_path)
        if img_cv is None:
            try:
                os.remove(file_path)
                removed_count += 1
                print(f"🗑️ Removed corrupt image (OpenCV failed): {file_path}")
            except Exception:
                pass
            continue

        # Test 2: Try decoding via TensorFlow raw decoder
        try:
            raw_bytes = tf.io.read_file(file_path)
            _ = tf.io.decode_image(raw_bytes, channels=3)
        except Exception:
            try:
                os.remove(file_path)
                removed_count += 1
                print(f"🗑️ Removed corrupt image (TF decode failed): {file_path}")
            except Exception:
                pass

print(f"✅ Scanning complete! Total corrupt/invalid files deleted: {removed_count}")

# 2. Native Dataset Loader
print("📸 Loading dataset...")
train_ds = tf.keras.utils.image_dataset_from_directory(
    SOIL_DATASET_DIR,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical"
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    SOIL_DATASET_DIR,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical"
)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

# 3. Augmentation
data_augmentation = Sequential([
    layers.Rescaling(1./255),
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
    layers.RandomContrast(0.2)
], name="data_augmentation")

rescaling_only = Sequential([
    layers.Rescaling(1./255)
], name="rescaling_only")

train_ds = train_ds.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=AUTOTUNE)
val_ds = val_ds.map(lambda x, y: (rescaling_only(x), y), num_parallel_calls=AUTOTUNE)

# 4. Model Setup
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = True

for layer in base_model.layers[:-30]:
    layer.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(NUM_CLASSES, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

output_h5_path = os.path.join(CHECKPOINTS_DIR, "soil_classifier_7class.h5")

callbacks = [
    ModelCheckpoint(output_h5_path, monitor='val_accuracy', save_best_only=True, verbose=1),
    EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=1)
]

print("\n🏋️ Training CNN Model for 50 Epochs...")
model.fit(
    train_ds,
    epochs=EPOCHS,
    validation_data=val_ds,
    callbacks=callbacks
)

print(f"\n🎉 High Accuracy Model Saved Successfully at:\n   {output_h5_path}")