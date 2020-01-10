import numpy as np


def sigmoid(x, deriv=False):
    if deriv:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


class NeuralNetwork:

    def __init__(self, inputs, hidden, outputs, learning_rate=0.05, activation=sigmoid):
        # temporary for debug porpoises
        np.random.seed(1)
        # set network parameters
        self.inputs = inputs
        self.hidden = hidden
        self.outputs = outputs
        self.learning_rate = learning_rate
        self.activation = activation
        # initialize weights ( matrices with values between -1 and 1)
        self.hidden_weights = 2 * np.random.random((hidden, inputs)) - 1
        self.output_weights = 2 * np.random.random((outputs, hidden)) - 1
        # initialize biases (arrays with values between -1 and 1)
        self.hidden_biases = 2 * np.random.rand(hidden) - 1
        self.output_biases = 2 * np.random.rand(outputs) - 1

    def feed_forward(self, input_array):
        # Calculate hidden layer's output
        hidden = np.dot(self.hidden_weights, input_array)
        hidden = hidden + self.hidden_biases
        hidden = self.activation(hidden)

        # Calculate output's layer output (final result)
        output = np.dot(self.output_weights, hidden)
        output = output + self.output_biases
        output = self.activation(output)

        # return final result (array)
        return output

    # Choo choo!
    def train(self, input_array, target_array):
        # FEED FORWARD ALGORITHM:
        # Calculate hidden layer's output
        hidden = np.dot(self.hidden_weights, input_array)
        hidden = hidden + self.hidden_biases
        hidden = self.activation(hidden)

        # Calculate output's layer output (final result)
        output = np.dot(self.output_weights, hidden)
        output = output + self.output_biases
        output = self.activation(output)

        # ERRORS CALCULATING
        output_errors = target_array - output
        hidden_errors = self.output_weights.T.dot(output_errors)

        # BACKPROPAGATION
        # Calculate the output layer's gradients
        output_gradients = self.activation(output, deriv=True)
        output_gradients = np.multiply(output_gradients, output_errors)
        output_gradients = np.multiply(output_gradients, self.learning_rate)

        # Calculate the output layer's deltas
        output_deltas = np.dot(np.array([output_gradients]).T, np.array([hidden]))

        # Adjusting output layer's weights and biases
        self.output_weights = self.output_weights + output_deltas
        self.output_biases = self.output_biases + output_gradients

        # Calculate the hidden layer's gradients
        hidden_gradients = self.activation(hidden, deriv=True)
        hidden_gradients = np.multiply(hidden_gradients, hidden_errors)
        hidden_gradients = np.multiply(hidden_gradients, self.learning_rate)

        # Calculate the hidden layer's deltas
        hidden_deltas = np.dot(np.array([hidden_gradients]).T, np.array([input_array]))

        # Adjusting hidden layer's weights and biases
        self.hidden_weights = self.hidden_weights + hidden_deltas
        self.hidden_biases = self.hidden_biases + hidden_gradients

        return (1./2.*len(target_array))*np.sum(np.square(output_errors))