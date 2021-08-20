#logreg_using_tensorflow

import tensorflow as tf
import numpy as np

#initialise parameters
#logreg... W of shape (1,n_x) and b of shape (1,1)
def initialise_parameters(n_x):
	W=tf.Variable(np.random.rand(1,n_x))
	b=tf.Variable(np.zeros((1,1)))
	parameters={"W":W,"b":b}
	return parameters

#sigmoid
def sigmoid(Z):
	return 1/(1+tf.exp(-Z))

#do forward_prop
def forward_prop(X,parameters):
	Z=tf.add(tf.matmul(W,X),b)
	A=sigmoid(Z)
	return A

def logreg_model(X_train,Y_train,learning_rate=5.,no_of_epochs=1000):
	n_x,m=X_train.shape
	X=tf.placeholder(dtype=tf.float64)
	Y=tf.placeholder(dtype=tf.float64)
	W=tf.Variable(np.random.rand(1,n_x))
	b=tf.Variable(np.zeros((1,1)))
	Z=tf.add(tf.matmul(W,X),b)
	A=sigmoid(Z)
	cost=tf.reduce_sum(-(Y*tf.log(A)+(1-Y)*tf.log(1-A)))/m
	optimizer=tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
	init=tf.global_variables_initializer()
	cost_list=[]
	with tf.Session() as sess:
		sess.run(init)
		for epoch in range(0,no_of_epochs):
			epoch_cost,_=sess.run([cost,optimizer],feed_dict={X:X_train,Y:Y_train})
			if epoch%200==0:
				cost_list.append(epoch_cost)
		parameters={"W":W,"b":b}
		model_dict={"parameters":sess.run(parameters),"learning_rate":learning_rate,"no_of_epochs":no_of_epochs,"cost_list":cost_list}
	return model_dict

X=np.array([	[ 0., 1., 0., 1., 0., 1., 0., 1.],
		[ 0., 0., 1., 1., 0., 0., 1., 1.],
		[ 0., 0., 0., 0., 1., 1., 1., 1.]])
Y=np.array([	[ 0., 1., 1., 1., 1., 1., 1., 1.]])

model = logreg_model(X,Y)
for key in model.keys():
	print(key)
	if(type(model[key]) == type({})):
		for key1 in model[key].keys():
			print(key1)
			print(model[key][key1])
	elif(type(model[key]) == type([])):
		print(np.array(model[key]).reshape(-1, 1))
	else:
		print(model[key])
	
		
