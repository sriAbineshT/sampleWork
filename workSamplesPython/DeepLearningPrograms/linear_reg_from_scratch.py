class LinearRegression:
	import numpy as np
	def feed_training_data(self,X_train,y_train):#use after creating an object and only once
		self.X_train=X_train
		self.y_train=y_train
		self.input_layer=X_train
		self.coef=np.zeros((X_train.shape[1],1))
		self.bias=0.
		self.no_of_observations=X_train.shape[0]
	def obtain_output_layer(self):#dont use this from outside class
		self.output_layer=np.dot(self.X_train,self.coef)+self.bias
	def error_with_training_data(self):#returns the mean of sum of squares of individual errors in training phase
		return np.sum((self.output_layer-self.y_train)**2)/self.no_of_observations
	def train_and_update(self,learning_rate=.00001,no_of_steps=100000,allowable_error=0):#use only after feeding training data
		self.obtain_output_layer()	
		for step in range(0,no_of_steps):
			if self.error_with_training_data()<=allowable_error:
				break
			d_coef=-(2/self.no_of_observations)*(np.dot(X_train.T,(self.output_layer-self.y_train))).sum(axis=1)*learning_rate
			d_bias=-(2/self.no_of_observations)*np.sum(self.output_layer-self.y_train)*learning_rate
			self.coef+=d_coef
			self.bias+=d_bias
			self.obtain_output_layer()
			

import numpy as np
X_train=np.array([[1],[2],[3]])
y_train=np.array([[3.14],[6.3],[9.4]])
model=LinearRegression()
model.feed_training_data(X_train,y_train)
model.train_and_update(learning_rate=.01,no_of_steps=1000,allowable_error=0)
print("model_input_layer")
print(model.input_layer)
print("model_weights")
print(model.coef)
print("model_bias")
print(model.bias)
print("modle_output_layer")
print(model.output_layer)
print("model_error")
print(model.error_with_training_data())


