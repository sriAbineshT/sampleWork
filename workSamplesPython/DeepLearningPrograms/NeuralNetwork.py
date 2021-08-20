import numpy as np

def activationfunction(array):#LeakyRectifiedLinearActivation
	return np.where(array<0,0,array)

def activationfunction_derivative(array):
	return np.where(array<0,0,1)

class NeuralNetwork():
	n_neurons1=5
	n_neurons2=5
	learning_rate=.001
	def __init__(self,X_train,y_train):
		self.X_train=X_train
		self.y_train=y_train
		self.input_layer=self.X_train
		self.weights1=np.random.rand(self.X_train.shape[1],self.n_neurons1)
		self.weights2=np.random.rand(self.n_neurons1,self.n_neurons2)
		self.weights3=np.random.rand(self.n_neurons2,self.y_train.shape[1])
	def feedforward(self):
		self.layer1=activationfunction(np.dot(self.input_layer,self.weights1))
		self.layer2=activationfunction(np.dot(self.layer1,self.weights2))
		self.output_layer=np.dot(self.layer2,self.weights3)
	def lossfunction(self):
		return np.sum((self.y_train-self.output_layer)*(self.y_train-self.output_layer),axis=0)/self.y_train.shape[0]
	def backpropagate(self):
		d_weights3=self.learning_rate*np.dot(self.layer2.T,(self.y_train-self.output_layer))
		d_weights2=self.learning_rate*np.dot(self.layer1.T,np.dot((self.y_train-self.output_layer),self.weights3.T)*activationfunction_derivative(np.dot(self.layer1,self.weights2)))
		d_weights1=self.learning_rate*np.dot(self.input_layer.T,np.dot(np.dot((self.y_train-self.output_layer),self.weights3.T)*activationfunction_derivative(np.dot(self.layer1,self.weights2)),self.weights2.T)*activationfunction_derivative(np.dot(self.input_layer,self.weights1)))
		self.weights1+=d_weights1
		self.weights2+=d_weights2
		self.weights3+=d_weights3

X=np.array([[1],[2],[3]])
y=np.array([[1],[1.5],[2]])

NN=NeuralNetwork(X,y)
NN.feedforward()
for n in range(1000):
	NN.backpropagate()
	NN.feedforward()
print("model_X_train")
print(NN.input_layer)
print("model_y_train")
print(NN.y_train)
print("modle_y_predict")
print(NN.output_layer)
print("model_error")
print(NN.lossfunction())





