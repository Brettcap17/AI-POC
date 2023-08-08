from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import pandas as pd
import time

pd.set_option("display.max_columns", None)

# global vars
dir_path = "output"
question = "How can I change my default search selection in Designer"

# Build a dictionary mapping the filepath of each file to the contents
def getDictionary():
  filenames = {}

  for file_path in os.listdir(dir_path):
    # check if current file_path is a file
    if os.path.isfile(os.path.join(dir_path, file_path)):
      # get file contents
      file_contents = ""
      with open(os.path.join(dir_path, file_path), "r") as f:
        for line in f:
          stripped_line = line.strip()
          file_contents += stripped_line
      # map from name to contents
      filenames[file_path] = file_contents

  filenames["question"] = question
  vector_matrix = vectorize(filenames)
  calculateAndOutput(vector_matrix, filenames)

# Vectorize the file contents
def vectorize(filenames):
  count_vectorizer = CountVectorizer()
  vector_matrix = count_vectorizer.fit_transform(list(filenames.values()))
  return vector_matrix

def create_dataframe(matrix, tokens, filenames):
  doc_names = list(filenames.keys())
  df = pd.DataFrame(data=matrix, index=doc_names, columns=tokens)
  return df

# Calculate and output the cosine similarity matrix between the question
# and the files
def calculateAndOutput(vector_matrix, filenames):
  start_time = time.time()
  cosine_similarity_matrix = cosine_similarity(vector_matrix)
  df = create_dataframe(cosine_similarity_matrix, list(filenames.keys()), filenames)
  end_time = time.time()
  print("Asked question: ", question)
  print("Total time (in sec):", end_time - start_time)
  with pd.option_context("display.max_rows", None, "display.max_columns", None):
    print(df.loc[:, ["question"]].sort_values(by=["question"]))

getDictionary()