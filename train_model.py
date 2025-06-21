import fasttext

# Train a supervised model
model = fasttext.train_supervised(
    input="training_data.txt",
    lr=1.0,
    epoch=25,
    wordNgrams=2,
    verbose=2,
    loss='softmax'
)

# Save model
model.save_model("model.ftz")