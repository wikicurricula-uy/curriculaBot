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


#sottodominio di lingua, da utilizzare per le chiamate API
lingua = "es"

idwikidata = 1

dimensione = 1

primoEdit = 1

note         =  1

immagini  = 1

visualizzazioni = 1

dimensioneIncipit = 1

dimensioneDiscussione = 1
#prefisso della pagina di discussione
discussione = "Discusión:"
discussioneURL = urllib.parse.quote(discussione)

#de momento, el conteo de avisos no funciona para la wikipedia en español
configAvvisi = 0

paginaCommons = 1

galleriaCommons = 1

itwikisource = 1

wikiversita = 1

wikibooks = 1

vetrina = 1
#vetrina template
vetrinaTemplate="{{artículo destacado"

qualita = 1
#voce di qualita template
vdqTemplate="{{artículo bueno"

vaglio = 1

bibliografia = 1

coordinate = 1


def get_avg_pageviews(voce, start, end):
  SOMMA = 0;

  try:

    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+lingua+".wikipedia/all-access/user/"+voce+"/daily/"+start+"/"+end
   
    html = urlopen(url).read()



    html = str(html);

    html = html.replace('{"items":[',"")

    html = html.replace(']}',"")

    n = html.count("}")



    for i in range(n):

       txt = html[:html.find("}")+1]

       SOMMA += int(txt[txt.find('"views":')+len('"views":'):-1])

       html =html.replace(txt,"",1)
    
    d1 = datetime.strptime(start, "%Y%m%d")
    d2 = datetime.strptime(end, "%Y%m%d")
    giorni = (abs((d2 - d1).days)+1)
    ris = str(int(round((SOMMA/giorni),0)))

  except:

    ris = "ERRORE"
  
  return ris

# returns visits since the beginning of time, average dayly visits since the begininning of time, average daily visits in the specified year
def visite(voce):

  #YYYYMMGG
  START_ALL_TIME = "20150701"; 

  START_PREV_YEAR = "20220101";
  END_PREV_YEAR = "20221231";

  START_CURRENT_YEAR = "20230101";
  END_CURRENT_YEAR   = "20230831";  

  DATE = []


  #calculate ris1, total pageviews since the beginning of time, and ris2, average pageviews since de beginning of time
  d1 = datetime.strptime(START_ALL_TIME, "%Y%m%d")

  d2 = datetime.strptime(END_CURRENT_YEAR, "%Y%m%d")

  giorni = (abs((d2 - d1).days)+1)

  VOCE = voce.replace(" ","_")

  SOMMA = 0

  try:

    url ="https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"+lingua+".wikipedia/all-access/user/"+VOCE+"/daily/"+START_ALL_TIME +"/" + END_CURRENT_YEAR

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

  #calculate ris3, average pageviews from previous year
  ris3 = get_avg_pageviews(VOCE, START_PREV_YEAR, END_PREV_YEAR)

  #calculate ris4, average pageviews from current year
  ris4 = get_avg_pageviews(VOCE, START_CURRENT_YEAR, END_CURRENT_YEAR)

   
  return str(ris1), str(ris2), str(ris3), str(ris4)





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

    url ="https://xtools.wmflabs.org/api/page/articleinfo/"+lingua+".wikipedia.org/"+voce.replace(" ","_")
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

   if vdqTemplate in text.lower():

      return "1"

   else:

      return "0"



def vetrina(text):

   if vetrinaTemplate in text.lower():

      return "1"

   else:

      return "0"





    

def analisi():
   f = open('query.csv', "r")

   vox = f.readlines()   
    
   # eliminare il contenuto del file prima di iniziare
   resultati = open('resultati.txt',"w")
   resultati.truncate(0)
   resultati.close()

   for voce in vox:
      
      resultati = open('resultati.txt', 'a')  # aprire il file in modalità di aggiunta

      flag = 1

      voce = voce[:-1]

      voce = voce.replace(" ","_")

      ris = ""

      wikitext = ""



      voce2 = urllib.parse.quote(voce)

      voce = voce.replace(" ","_")


      try:

        url = "https://"+lingua+".wikipedia.org/w/api.php?action=parse&page=" + voce2 + "&prop=wikitext&formatversion=2&format=json"

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

        url = "https://"+lingua+".wikipedia.org/w/api.php?action=query&titles=" + voce2 +"&prop=pageprops&format=json&formatversion=2"

        json_url = urlopen(url)

        data = json.loads(json_url.read())

        wikidataid = data["query"]["pages"][0]["pageprops"]["wikibase_item"]

        url ="https://www.wikidata.org/wiki/Special:EntityData/"+wikidataid+".json"

        json_url = urlopen(url)

        wikidata = json.loads(json_url.read())



        url = "https://"+lingua+".wikipedia.org/w/api.php?action=parse&page=" + voce2 + "&prop=wikitext&formatversion=2&format=json"

        json_url = urlopen(url)

        data = json.loads(json_url.read())

        wikitext = data["parse"]["wikitext"]



        try:

          url = "https://"+lingua+".wikipedia.org/w/api.php?action=parse&page=" + discussioneURL + voce2 + "&prop=wikitext&formatversion=2&format=json"
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

           

        if configAvvisi:

           for i in avvisi(wikitext):
              print("some avisi")
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

      resultati.write(ris + "\n")  # aggiungere un salto di linea dopo ogni risultato
      resultati.close()  # chiudere il file
      print (ris)

     

def main():

   analisi()



if __name__ == "__main__":

   main()