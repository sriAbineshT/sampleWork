import numpy as np

def relu(Z):
	return np.where(Z>0,Z,0)

def relu_backward(A):
	return np.where(A>0,1,0)

def sigmoid(Z):
	return 1/(1+np.exp(-Z))

def neural_network_binary_classifier(X_train,Y_train,X_test,Y_test,hidden_layer_sizes=(),learning_rate=.01,num_iterations=1000):
	layer_sizes=(X_train.shape[0],)+hidden_layer_sizes+(1,) 
	L=len(layer_sizes)-1
	parameters={}	
	grads={}
	for l in range(1,L+1):
		parameters["W"+str(l)]=np.random.randn(layer_sizes[l],layer_sizes[l-1])*.01
		parameters["b"+str(l)]=np.zeros((layer_sizes[l],1))
	
	m=Y_train.shape[1]
	training_costs=[]
	for i in range(num_iterations):
		cache={}
		A=X_train
		cache["A"+str(0)]=A
		for l in range(1,L):
			Z=np.dot(parameters["W"+str(l)],A)+parameters["b"+str(l)]
			A=relu(Z)
			cache["Z"+str(l)]=Z
			cache["A"+str(l)]=A
		Z=np.dot(parameters["W"+str(L)],A)+parameters["b"+str(L)]
		A=sigmoid(Z)
		cache["Z"+str(L)]=Z
		cache["A"+str(L)]=A
		
		if i%100==0:
			cost=np.sum(-(Y*np.log(A)+(1-Y)*np.log(1-A)))/m
			training_costs.append(cost)

		dZ=(cache["A"+str(L)]-Y_train)/m
		for l in reversed(range(1,L+1)):
			A=cache["A"+str(l-1)]
			dW=np.dot(dZ,A.T)
			db=np.sum(dZ,axis=1,keepdims=True)
			dZ=np.dot(parameters["W"+str(l)].T,dZ)*relu_backward(A)
			parameters["W"+str(l)]-=learning_rate*dW
			parameters["b"+str(l)]-=learning_rate*db
			if i==num_iterations-1:
				grads["dW"+str(l)]=dW
				grads["db"+str(l)]=db
		
	AL=cache["A"+str(L)]	
	Y_prediction_train=np.where(AL>.5,1,0)

	A=X_test
	for l in range(1,L):
		Z=np.dot(parameters["W"+str(l)],A)+parameters["b"+str(l)]
		A=relu(Z)
	Z=np.dot(parameters["W"+str(L)],A)+parameters["b"+str(L)]
	AL=sigmoid(Z)
	Y_prediction_test=np.where(AL>.5,1,0)
	
	d={	"parameters":parameters,
		"Y_prediction_train":Y_prediction_train,
		"Y_prediction_test":Y_prediction_test,
		"training_costs":training_costs,
		"grads":grads}	

	return d

X=np.array([	[ 0, 1, 0, 1, 0, 1, 0, 1],
		[ 0, 0, 1 ,1, 0, 0, 1 ,1],
		[ 0, 0, 0, 0, 1, 1, 1, 1]])
Y=np.array([	[ 0, 1, 1, 1, 1, 1, 1, 1]])

model=neural_network_binary_classifier(X,Y,X,Y,hidden_layer_sizes=(),learning_rate=1,num_iterations=30000)
for key in model.keys():
	print(key)
	if(type(model[key]) == type({})):
		for key1 in model[key].keys():
			print(key1)
			print(model[key][key1])
	if(type(model[key]) == type([])):
		print(np.array(model[key]).reshape(-1, 1))
	if(type(model[key]) == type(np.array([]))):
		print(model[key])
	

	
		
		


