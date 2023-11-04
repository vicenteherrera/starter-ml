from transformers import pipeline

print("")
print("SENTIMENT-ANALYSIS")
classifier = pipeline("sentiment-analysis")
result = classifier("I've been waiting for a HuggingFace course my whole life.")
print("%s" % result)
print("")

print("ZERO-SHOT-CLASSIFICATION")
classifier = pipeline("zero-shot-classification")
result = classifier(
    "This is a course about the Transformers library",
    candidate_labels=["education", "politics", "business"],
)
print("%s" % result)
print("")

print("TEXT GENERATOR (default model)")
generator = pipeline("text-generation")
result = generator("In this course, we will teach you how to")
print("%s" % result)
print("")

print("TEXT GENERATOR (distilgpt2)")
generator = pipeline("text-generation", model="distilgpt2")
result = generator(
    "In this course, we will teach you how to",
    max_length=30,
    num_return_sequences=2,
)
print("%s" % result)
print("")