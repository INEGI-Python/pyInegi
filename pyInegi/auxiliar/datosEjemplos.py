
class paramMzas:
   def __init__(self,file,dist,out,rows=-1,prev=0):
      self.file=file
      self.dist=dist
      self.out=out
      self.rows=rows
      self.prev=prev

def features(dato):
   return {"mzas": "https://github.com/INEGI-Python/pyInegi/raw/d248d3a43c65915c7a3e64396cd6da57c65ad093/datosEjemplo/cartografiaUrbana.gdb",
           "costa-acapulco": "https://github.com/INEGI-Python/pyInegi/raw/41e30bb0f3c568d5ff981560a18aeeafac77c039/datosEjemplo/osta-acapulco.shp"
   }[dato]


