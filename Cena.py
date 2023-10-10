import FreeCAD, FreeCADGui, Part
from pivy import coin

class Cena:
	def __init__(self, obj):
		obj.Proxy = self

		
		
		obj.addProperty("App::PropertyInteger","Indice","Ordem","Indice da cena para a animação").Indice = 1
		
		obj.addProperty("App::PropertyBool","ActiveScene","Scene","Coloca a camera na posição da cena").ActiveScene = False

		obj.addProperty("App::PropertyFloatList","Posicao","Parametros","Parametro de cena")
		obj.addProperty("App::PropertyFloatList","Direcao","Parametros","Parametro de cena")
		obj.addProperty("App::PropertyFloat","Height","Parametros","Parametro de cena")
		obj.addProperty("App::PropertyFloat","FarDistance","Parametros","Parametro de cena")
		obj.addProperty("App::PropertyFloat","NearDistance","Parametros","Parametro de cena")
		obj.addProperty("App::PropertyFloat","AspectRatio","Parametros","Parametro de cena")
		obj.addProperty("App::PropertyFloat","FocalDistance","Parametros","Parametro de cena")
		obj.addProperty("App::PropertyString","CameraType","Parametros","Parametro de cena")

	
	def execute(self, obj):
		if obj.ActiveScene == False:
			rotacao = FreeCADGui.ActiveDocument.ActiveView.viewPosition().Rotation.Q
			obj.Direcao = [rotacao[0], rotacao[1], rotacao[2], rotacao[3]]

			posicao = FreeCADGui.ActiveDocument.ActiveView.viewPosition().Base
			obj.Posicao = [posicao[0], posicao[1], posicao[2]]

			cam = FreeCADGui.ActiveDocument.ActiveView.getCameraNode()

			if FreeCADGui.ActiveDocument.ActiveView.getCameraType() != 'Perspective':
				obj.Height = cam.height.getValue()
			else:
				obj.Height = cam.heightAngle.getValue()

			obj.FarDistance = cam.farDistance.getValue()
			obj.NearDistance = cam.nearDistance.getValue()
			obj.AspectRatio = cam.aspectRatio.getValue()
			obj.FocalDistance = cam.focalDistance.getValue()
			obj.CameraType = FreeCADGui.ActiveDocument.ActiveView.getCameraType()
		
		else: # executa quando a for  abilitado para executar em Scene

			FreeCADGui.ActiveDocument.ActiveView.setCameraType(obj.CameraType)
			transition = False

			if FreeCADGui.ActiveDocument.ActiveView.isAnimationEnabled() == True:
				transition = True
				FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(False) # Desativa a animação da camera.

			#Posiciona a direção da camera
			rot = App.Rotation(obj.Direcao[0], obj.Direcao[1], obj.Direcao[2], obj.Direcao[3]) #Cria um objeto de rotação
			FreeCADGui.ActiveDocument.ActiveView.setCameraOrientation(rot) # seta o objeto de rotação da camera

			# Posiciona a camera nas coordenadas armazenadas
			cam = FreeCADGui.ActiveDocument.ActiveView.getCameraNode()
			
			if FreeCADGui.ActiveDocument.ActiveView.getCameraType() != 'Perspective':
				cam.height.setValue(obj.Height)
			else:
				cam.heightAngle.setValue(obj.Height)


			cam.aspectRatio.setValue(obj.AspectRatio)
			cam.focalDistance.setValue(obj.FocalDistance)

			cam.farDistance.setValue(obj.FarDistance)
			cam.nearDistance.setValue(obj.NearDistance)
			cam.position.setValue(obj.Posicao[0],obj.Posicao[1],obj.Posicao[2])

			obj.ActiveScene = False

			#Reativa a animação da cemra 
			if transition == True: FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(True) 






def createSena():
	obj = FreeCAD.ActiveDocument.addObject('Part::FeaturePython','Cena')

	cena = Cena(obj)


createSena()