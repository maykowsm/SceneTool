import FreeCAD, FreeCADGui, Part
import copy, time

fps = 60 #(q/s)
timeScene = 5 #Tempo de execuçaõ entre as cenas (s)
sleep = 5  #Tempo de pausa entre uma cena e outra (s)

steps = timeScene * fps #Numero de passos entre cada cena (velocidade de transição)
timee = 1/fps #Tempo enter os qadros de transição das cenas


 

'''Função que retorna uma lista com todos os objetos cena do projeto, ou com as cenas celecionadas'''
def getScene():
	listScene = []
	listScene = Gui.Selection.getSelection()

	if len(listScene) == 0:
		objects = FreeCAD.ActiveDocument.Objects

		listScene = []
		for obj in objects:
			try:
				if obj.Indice > 0:
					listScene.append(obj)
			except:
				pass

	if len(listScene) == 0:
		print('Não foram identificados objetos de cena no documento, por favor crie objetos de cena no doocumento.')

	else:
		return listScene

#entrada com o objeto cena, retorna um vetor com todos os parametros da camera
def getParameters(scene):
	parameters = [scene.Posicao, scene.Direcao, scene.Height, scene.FarDistance, scene.NearDistance, scene.AspectRatio, scene.FocalDistance]
	return parameters

#Pega os parametros atuais da camera
def getCam():
	parameters = []
	posicao = FreeCADGui.ActiveDocument.ActiveView.viewPosition().Base
	parameters.append([posicao[0], posicao[1], posicao[2]])

	rotacao = FreeCADGui.ActiveDocument.ActiveView.viewPosition().Rotation.Q
	parameters.append([rotacao[0], rotacao[1], rotacao[2], rotacao[3]])

	cam = FreeCADGui.ActiveDocument.ActiveView.getCameraNode()

	if FreeCADGui.ActiveDocument.ActiveView.getCameraType() != 'Perspective':
		parameters.append(cam.height.getValue())
	else:
		parameters.append(cam.heightAngle.getValue())

	parameters.append(cam.farDistance.getValue())
	parameters.append(cam.nearDistance.getValue())
	parameters.append(cam.aspectRatio.getValue())
	parameters.append(cam.focalDistance.getValue())

	return parameters

#Retorna um vetor com c/ tamanho dos passos de cada parâmetro da camera
def getSteps(scene1, scene2):
	listSteps = []

	listSteps.append([(scene2[0][0]- scene1[0][0])/steps, (scene2[0][1]- scene1[0][1])/steps, (scene2[0][2]- scene1[0][2])/steps])
	listSteps.append([(scene2[1][0]- scene1[1][0])/steps, (scene2[1][1]- scene1[1][1])/steps, (scene2[1][2]- scene1[1][2])/steps,(scene2[1][3]- scene1[1][3])/steps])

	for i in range(2, len(scene1)):
		listSteps.append((scene2[i] - scene1[i])/steps)

	return listSteps


#Função que executa a transição entre todas as cenas do projeto 
def animation():

	'''salva o estado da função de animação de cena do FreeCAD e a desativa temporariamente para executar a animação'''
	transition = False
	if FreeCADGui.ActiveDocument.ActiveView.isAnimationEnabled() == True:
		transition = True
		FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(False) # Desativa a animação da camera.
	

	listScene = getScene()
	if listScene == None:
		return 

	scene1 = ''
	scene2 = getCam()

	for i in range(len(listScene)):
		
		scene1 = copy.copy(scene2)
		scene2 = getParameters(listScene[i])

		parameter_steps = getSteps(scene1, scene2)
		FreeCADGui.ActiveDocument.ActiveView.setCameraType(listScene[i].CameraType)

		for j in range(steps+1):
			parameters_cam = getCam()


			rot = App.Rotation(parameters_cam[1][0]+parameter_steps[1][0], parameters_cam[1][1]+parameter_steps[1][1], parameters_cam[1][2]+parameter_steps[1][2], parameters_cam[1][3]+parameter_steps[1][3])#Cria um objeto de rotação
			FreeCADGui.ActiveDocument.ActiveView.setCameraOrientation(rot) #Seta o objeto de rotação da camera

			cam = FreeCADGui.ActiveDocument.ActiveView.getCameraNode() # cria o objeto camera para setar os demais parâmetros

			if FreeCADGui.ActiveDocument.ActiveView.getCameraType() != 'Perspective':
				cam.height.setValue(parameters_cam[2]+parameter_steps[2])
			else:
				cam.heightAngle.setValue(parameters_cam[2]+parameter_steps[2])

			cam.aspectRatio.setValue(parameters_cam[5]+parameter_steps[5])
			cam.focalDistance.setValue(parameters_cam[6]+parameter_steps[6])

			cam.farDistance.setValue(parameters_cam[3]+parameter_steps[3])
			cam.nearDistance.setValue(parameters_cam[4]+parameter_steps[4])
			cam.position.setValue(parameters_cam[0][0]+parameter_steps[0][0], parameters_cam[0][1]+parameter_steps[0][1], parameters_cam[0][2]+parameter_steps[0][2])

			#FreeCAD.ActiveDocument.recompute()
			FreeCADGui.updateGui()
			time.sleep(timee)

	#Reativa a animação da cemra 
	if transition == True: FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(True) 




		


animation()