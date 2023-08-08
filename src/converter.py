from bs4 import BeautifulSoup
from markdown import markdown
import os

def main():
  outputDir = '../output'

  if not os.path.exists(outputDir):
    os.mkdir(outputDir)

  dirs = os.listdir('../docs/collection_docs/')
  for dir in dirs:
    dir ='../docs/collection_docs/' + dir + '/'
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
