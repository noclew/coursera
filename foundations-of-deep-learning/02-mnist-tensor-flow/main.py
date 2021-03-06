# This is mostly an example of how easy it is to start out with Tensor
# Flow!

import os.path
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# Download MNIST data.
mnist = input_data.read_data_sets(".", one_hot=True, reshape=False)

# Parameters
learning_rate = 0.1
training_epochs = 10
batch_size = 1
display_step = 1

# MNIST input is 28*28=784, and there are 10 digits.
n_input = 784
n_classes = 10

# Number of units in each hidden layer.
n_hidden_layer1 = 510
n_hidden_layer2 = 203
n_hidden_layer3 = 203

# Store layers weight & bias
weights = {
    'hidden_layer': tf.Variable(
        tf.random_normal([n_input, n_hidden_layer1])
    ), 'hidden_layer2': tf.Variable(
        tf.random_normal([n_hidden_layer1, n_hidden_layer2])
    ), 'hidden_layer3': tf.Variable(
        tf.random_normal([n_hidden_layer2, n_hidden_layer3])
    ), 'out': tf.Variable(
        tf.random_normal([n_hidden_layer2, n_classes])
    )
}
biases = {
    'hidden_layer': tf.Variable(tf.random_normal([n_hidden_layer1])),
    'hidden_layer2': tf.Variable(tf.random_normal([n_hidden_layer2])),
    'hidden_layer3': tf.Variable(tf.random_normal([n_hidden_layer3])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# Placeholders for x and y data.
x = tf.placeholder("float", [None, 28, 28, 1])
y = tf.placeholder("float", [None, n_classes])
# Flatten x data.
x_flat = tf.reshape(x, [-1, n_input])

# Using sigmoid temporarily as an experiment with low batch sizes.
# Hidden layer with RELU activation
layer_1 = tf.add(
    tf.matmul(x_flat, weights['hidden_layer']), biases['hidden_layer']
)
layer_1 = tf.nn.sigmoid(layer_1)

# Hidden layer with RELU activation
layer_2 = tf.add(
    tf.matmul(layer_1, weights['hidden_layer2']), biases['hidden_layer2']
)
layer_2 = tf.nn.sigmoid(layer_2)

# Hidden layer with RELU activation
#layer_3 = tf.add(tf.matmul(layer_2, weights['hidden_layer3']), biases['hidden_layer3'])
#layer_3 = tf.nn.relu(layer_3)

# Output layer with linear activation
logits = tf.matmul(layer_2, weights['out']) + biases['out']

# Define loss and optimizer
cost = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y)
)
optimizer = tf.train.GradientDescentOptimizer(
    learning_rate=learning_rate
).minimize(cost)

# Run model on test data and calculate accuracy.
correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

def evaluate_validation_set():
    computed_cost = sess.run(
        cost, feed_dict={
            x: mnist.validation.images, y: mnist.validation.labels
        }
    )
    computed_accuracy = sess.run(
        accuracy, feed_dict={
            x: mnist.validation.images, y: mnist.validation.labels
        }
    )

    return computed_cost, computed_accuracy

EVALUATION_PER_BATCHES = 1000
def run_epoch(sess, epoch):
    num_batches = int(mnist.train.num_examples/batch_size)
    # Loop over all batches
    for batch_idx in range(num_batches):
        # Yay for global variables!
        batch_x, batch_y = mnist.train.next_batch(batch_size)
        # Perform optimization step.
        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})
        if ((batch_idx+1) % EVALUATION_PER_BATCHES == 0):
            computed_cost, computed_accuracy = evaluate_validation_set()
            print((
                f"Epoch: {epoch+1} | Batch: {batch_idx + 1}"
                f" cost={computed_cost:.3f} accuracy={computed_accuracy:.3f}"
            ))

    if epoch % display_step == 0:
        computed_cost, computed_accuracy = evaluate_validation_set()
        print((
            f">>>Epoch: {epoch+1}<<<"
            f" cost={computed_cost:.3f} accuracy={computed_accuracy:.3f}"
        ))

def run_training(sess):
    for epoch in range(training_epochs):
        run_epoch(sess, epoch)
    print("Optimization Finished!")

# Initializing the variables
init = tf.global_variables_initializer()
saver = tf.train.Saver()

MODEL_FNAME = "./model.ckpt"

# Launch the graph
with tf.Session() as sess:
    # This quickly loads the trained file if it already exists.
    ipt = input("Load old model?")
    if ipt != "no":
        saver.restore(sess, MODEL_FNAME)
    else:
        sess.run(init)

    run_training(sess)
    saver.save(sess, MODEL_FNAME)

    computed_test_accuracy = sess.run(accuracy, feed_dict={
        x: mnist.test.images,
        y: mnist.test.labels
    })
    print(f"Accuracy: {computed_test_accuracy:.3f}")
