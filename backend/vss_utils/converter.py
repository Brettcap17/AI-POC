from bs4 import BeautifulSoup
from markdown import markdown
import os

def main():
  outputDir = '../output'
  inputDir = '../docs/collection_docs/'

  if not os.path.exists(outputDir):
    os.mkdir(outputDir)

  dirs = os.listdir(inputDir)
  for dir in dirs:
    dir = inputdir + dir + '/'
    for file in os.listdir(dir):
      print(dir + file)
      if file.endswith('.md'):
        fileOut = open(f'{outputDir}/{file.removesuffix(".md")}.txt', 'w')

        fileContents = open(dir + file, 'r').read()
        html = markdown(fileContents)
        text = ''.join(BeautifulSoup(html).findAll(text=True))

        fileOut.write(text)
        fileOut.close()

main()
