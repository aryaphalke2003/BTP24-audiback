import requests
import tqdm
import json
  
# api-endpoint
  
for i in range(0, 63):
    # URL = "http://127.0.0.1:8000/audiofiles/audiofiles/id/"
    URL = "http://127.0.0.1:8000/audiofiles/audiofiles/id/"

    
    try :
       
      URL = URL + str(i)
      print(URL)
      r = requests.get(url = URL)
      data = r.json()

      chapter = data['ChapterName']
      pdf_url = data['PDF']
      audio_url = data['AudioFile']

      r = requests.get(pdf_url)
      with open(f"data-backup/pdfs/{chapter}.pdf",'wb') as f:
        f.write(r.content)
      
      r = requests.get(audio_url)
      with open(f"data-backup/audiofiles/{chapter}.mp3",'wb') as f:
        f.write(r.content)
    except:
       print("Error")

  