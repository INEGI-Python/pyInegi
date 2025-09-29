
class parametros:
   def __init__(self,file,dist,web=0,rows=None):
      self.file=file
      self.dist=dist
      self.rows=rows
      self.web=web

def shapes(dato):
   return {"mzas": "https://github.com/INEGI-Python/pyInegi/raw/41e30bb0f3c568d5ff981560a18aeeafac77c039/datosEjemplo/manzan.shp",
           "costa-acapulco": "https://github.com/INEGI-Python/pyInegi/raw/41e30bb0f3c568d5ff981560a18aeeafac77c039/datosEjemplo/osta-acapulco.shp"
   }[dato]