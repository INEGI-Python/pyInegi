class Datos:
   def __init__(self):
      self.files = None

   def ver(self):
      import os
      ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'DatosEntrada')
      self.files = os.listdir(ruta)
      return self.files





def features(dato):
   return {"mzas": "https://github.com/INEGI-Python/pyInegi/raw/d248d3a43c65915c7a3e64396cd6da57c65ad093/datosEjemplo/cartografiaUrbana.gdb",
           "costa-acapulco": "https://github.com/INEGI-Python/pyInegi/raw/41e30bb0f3c568d5ff981560a18aeeafac77c039/datosEjemplo/osta-acapulco.shp"
   }[dato]


