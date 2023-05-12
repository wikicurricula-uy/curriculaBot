import urllib
import sys
import calendar
import json
import datetime
from urllib.request import urlopen
import urllib.parse
import string
import json
from datetime import datetime


idwikidata = 1
dimensione = 1
primoEdit = 1
note         =  1
immagini  = 1
primoEdit = 1
visualizzazioni = 1
dimensioneIncipit = 1
dimensioneDiscussione = 1
avvisi = 1
paginaCommons = 1
galleriaCommons = 1
itwikisource = 1
wikiversita = 1
wikibooks = 1
vetrina = 1
qualita = 1
vaglio = 1
bibliografia = 1
coordinate = 1


def visite(voce):

  #START = "20200101"; #YYYYMMGG
  START = "20150701"; #YYYYMMGG
  END   = "20211231";   #YYYYMMGG
  START2 = "20210101"; #YYYYMMGG
  END2   = "20211231";   #YYYYMMGG
  DATE = []

  d1 = datetime.strptime(START, "%Y%m%d")
  d2 = datetime.strptime(END, "%Y%m%d")
  giorni = (abs((d2 - d1).days)+1)

  VOCE = voce.replace(" ","_")
  VALORI = []
  SOMMA = 0
  try:
    url ="https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/it.wikipedia/all-access/user/"+VOCE+"/daily/"+START +"/" + END
    html = urlopen(url).read()
    ecc = 0 # da cambiare
    if ecc == 0:
      html = str(html)
      html = html.replace('{"items":[',"")
      html = html.replace(']}',"")
      n = html.count("}")

      for i in range(n):
         txt = html[:html.find("}")+1]
         SOMMA += int(txt[txt.find('"views":')+len('"views":'):-1])
         html =html.replace(txt,"",1)

      ris1 = str(SOMMA)
      ris2 = str(int(round((SOMMA/giorni),0)))
  except:
    ris1 = "ERRORE"
    ris2 = "ERRORE"
   
  VALORI = [];
  SOMMA = 0;
  try:
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/it.wikipedia/all-access/user/"+VOCE+"/daily/"+START2 +"/" + END2
    html = urlopen(url).read()

    html = str(html);
    html = html.replace('{"items":[',"")
    html = html.replace(']}',"")
    n = html.count("}")

    for i in range(n):
       txt = html[:html.find("}")+1]
       SOMMA += int(txt[txt.find('"views":')+len('"views":'):-1])
       html =html.replace(txt,"",1)
    ris3 = str(int(round((SOMMA/365),0)))
  except:
    ris3 = "ERRORE"
   
  return str(ris1), str(ris2), str(ris3)


def nome2Q(item):
  return item.getID()


def note(text):
  return str(text.count('</ref>'))


def dimensione(text):
  return str(len(text))


def immagini(text):
  t = text.lower()
  img = str(t.count('.jpg')+t.count('.svg')+t.count('.jpeg')+t.count('.png')+t.count('.tiff')+t.count('.gif')+t.count('.tif')+t.count('.xcf'))
  return img


def primoEdit(voce):
  try:
    url ="https://xtools.wmflabs.org/api/page/articleinfo/it.wikipedia.org/"+voce.replace(" ","_")
    html = urlopen(url).read()
    html = str(html)
    html = html[html.find("created_at")+len("created_at")+3:]
    html = html[:10]
  except:
    html= "ERRORE"
  return html


def avvisi(t):
   t_tmp =t
   t = t.replace("\n","")
   t = t.replace(" ","")
   t = t.lower()
    
   tmpcotrollare = t.count('{{c|') + t.count('{{c}}')
   tmpsinottico = t.count('{{tmp|')  + t.count('{{tmp}}')
   tmpaiutare = t.count('{{a|')
   tmpcorreggere = t.count('{{correggere')
   tmpcuriosita = t.count('{{curiosit')
   tmpdividere = t.count('{{d|') + t.count('{{d}')
   tmpfonti = t.count('{{f|')  + t.count('{{f}}')
   tmplocalismo = t.count('{{l|')  + t.count('{{l}}')
   tmpPOV = t.count('{{p|')  + t.count('{{p}}')
   tmpNN = t.count('{{nn|')  + t.count('{{nn}}')
   tmprecentismo = t.count('{{recentismo')
   tmpmanualisitco = t.count('{{stilemanualistico')
   tmptraduzione = t.count('{{t|')  + t.count('{{t}}')
   tmpwikificare = t.count('{{w|')  + t.count('{{w}}')
   tmpstub = t.count('{{s|')  + t.count('{{s}}')
   tmpstubsezione = t.count('{{stubsezione')
   tmpcontrolcopi = t.count('{{controlcopy')

   sommaavvisi = tmpcotrollare + tmpsinottico + tmpaiutare + tmpcorreggere + tmpcuriosita + tmpdividere + tmpfonti + tmplocalismo + tmpPOV
   sommaavvisi = sommaavvisi + tmpNN + tmprecentismo + tmpmanualisitco + tmptraduzione + tmpwikificare + tmpstub + tmpstubsezione + tmpcontrolcopi

   tmpsenzafonti = t.count('{{senzafonte') + t.count('{{citazionenecessaria') + t.count('{{senzafonte}}') + t.count('{{citazionenecessaria}}')
   tmpchiarire = t.count('{{chiarire') + t.count('{{chiarire}}')

   return str(sommaavvisi), str(tmpsenzafonti), str(tmpchiarire)


def trovatemplate(text):
      tmp = text[2:]
      tmp2 = text[2:]
      tmp = tmp[:tmp.find("}}")+2]
      if "{{" in tmp:
          tmp3 = tmp[tmp.find("{{"):]
          tmp2 = tmp2.replace(tmp3,"$$$$$$$$$$$$$$")

          tmp2 = tmp2[:tmp2.find("}}")+2]
          tmp2 = tmp2.replace("$$$$$$$$$$$$$$",tmp3)
          return tmp2
      return tmp


def lunghezzaIncipit(text):
   incipit = text
   incipit = incipit[:incipit.find("\n==")]
   ntemplate  =incipit.count('{{')
   incipitclear = incipit
   fn = incipit.count("{{formatnum:")
   for i in range(fn):
      tmp = incipit[incipit.find("{{formatnum:"):]
      tmp = tmp[:tmp.find("}}")+2]
      tmp2 = tmp.replace("{{formatnum:","")
      tmp2 = tmp2.replace("}}","")
      incipit = incipit.replace(tmp, tmp2)

   ntemplate = incipit.count("{{")
   for i in range(ntemplate):
      text = incipit[incipit.find("{{"):]
      template = trovatemplate(text)
      text = text.replace("{{"+template,"")
      incipit = incipit.replace("{{"+template,"")
   incipit = incipit.replace("</ref>","")
   n = incipit.count("<ref")
   for i in range(n):
      tmp = incipit[incipit.find("<ref"):]
      tmp = tmp[:tmp.find(">")+1]
      incipit = incipit.replace(tmp,"")
   incipit = incipit.replace("[[","")
   incipit = incipit.replace("]]","")
   incipit = incipit.replace("|","")
   lunincipit = len(incipit)
   return str(lunincipit)


def vdq(text):
   if "{{voce di qualit" in text.lower():
      return "1"
   else:
      return "0"

def vetrina(text):
   if "{{vetrina" in text.lower():
      return "1"
   else:
      return "0"


    
def analisi():
   f = open('LISTA.txt', "r")
   vox = f.readlines()   
   for voce in vox:
      flag = 1
      voce = voce[:-1]
      voce = voce.replace(" ","_")
      ris = ""
      wikitext = ""

      voce2 = urllib.parse.quote(voce)
      voce = voce.replace(" ","_")

      try:
        url = "https://it.wikipedia.org/w/api.php?action=parse&page=" + voce2 + "&prop=wikitext&formatversion=2&format=json"
        json_url = urlopen(url)
        data = json.loads(json_url.read())
        wikitext = data["parse"]["wikitext"]
        if "#RINVIA"  in wikitext:
     #   print (wikitext)
          voce2 = wikitext[wikitext.find("[[")+2:]
          voce2 = voce2[:voce2.find("]]")]
          voce = voce2
          voce2 = voce2.replace("_"," ")
      except:
        pass                                     
      try:
        voce2 = urllib.parse.quote(voce)
        voce = voce.replace(" ","_")
        url = "https://it.wikipedia.org/w/api.php?action=query&titles=" + voce2 +"&prop=pageprops&format=json&formatversion=2"
        json_url = urlopen(url)
        data = json.loads(json_url.read())
        wikidataid = data["query"]["pages"][0]["pageprops"]["wikibase_item"]

        url ="https://www.wikidata.org/wiki/Special:EntityData/"+wikidataid+".json"
        json_url = urlopen(url)
        wikidata = json.loads(json_url.read())

        url = "https://it.wikipedia.org/w/api.php?action=parse&page=" + voce2 + "&prop=wikitext&formatversion=2&format=json"
        json_url = urlopen(url)
        data = json.loads(json_url.read())
        wikitext = data["parse"]["wikitext"]

        try:
          url = "https://it.wikipedia.org/w/api.php?action=parse&page=discussione%3A"+ voce2 + "&prop=wikitext&formatversion=2&format=json"
          json_url = urlopen(url)
          data = json.loads(json_url.read())
          wikitext_discussione = data["parse"]["wikitext"]
        except:
          wikitext_discussione = ""

        ris = ris + voce + "\t"
        ris = ris + wikidataid + "\t"
      except:
        ris = ris + voce +"\t" +"Voce inesistente"
       
      else:
        if primoEdit:
           ris = ris + primoEdit(voce2) + "\t"

        if dimensione:
           ris = ris + dimensione(wikitext) + "\t"

        if immagini:
           ris = ris + immagini(wikitext) + "\t"

        if note:
           ris = ris + note(wikitext) + "\t"
           
        if avvisi:
           for i in avvisi(wikitext):
              ris = ris + i + "\t"
               
        if dimensioneDiscussione:
           ris = ris + dimensione(wikitext_discussione) + "\t"

        if dimensioneIncipit:
           ris = ris + lunghezzaIncipit(wikitext) + "\t"
           
        if visite:
           for i in visite(voce2):
              ris = ris + i + "\t"

        if vdq:
           ris = ris + vdq(wikitext) + "\t"

        if vetrina:
           ris = ris + vetrina(wikitext) + "\t"

        if galleriaCommons:
           try:
              ris = ris + wikidata["entities"][wikidataid]["claims"]["P373"][0]["mainsnak"]["datavalue"]["value"] + "\t"
           except:
              ris = ris + "" + "\t"

        if paginaCommons:
           try:
              ris = ris + wikidata["entities"][wikidataid]["claims"]["P935"][0]["mainsnak"]["datavalue"]["value"] + "\t"
           except:
              ris = ris + "" + "\t"
   
        if itwikisource:
           try:
              ris = ris + wikidata["entities"][wikidataid]["sitelinks"]["itwikisource"]["title"] + "\t"
           except:
              ris = ris + "\t"

        if coordinate:
           try:
              ris = ris + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["latitude"] + "\t"
              ris = ris + wikidata["entities"][wikidataid]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["longitude"] + "\t"
           except:
              ris = ris + "\t" + "\t"
         
      print (ris)
     
def main():
   analisi()

if __name__ == "__main__":
   main()