import numpy as np
import tensorflow as tf

from scattering_transform import scattering_transform


def scattering_classifier(features, labels, mode, params):
    """
    Do the following:
    1. configure model via tensorflow operations
    2. define loss function for training/evaluation
    3. define training operation/optimizer
    4. generate predictions
    5. return predictions/loss/train_op/eval_metric_ops in EstimatorSpec object

    features: dict containing features passed via input_fn
    labels: Tensor containing labels passed to the model via input_fn
    mode: train, evaluate or predict
    params: additional hyperparameters
    """


    js, J, L = params['js'], params['J'], params['L']
    features = features["x"]
    print("let's scatter!")
    scattering_coefficients = scattering_transform(features, js, J, L)
    print(scattering_coefficients)
    # batch_size = scattering_coefficients.get_shape().as_list()[0]
    # throw all coefficients into single vector for each image
    # scattering_coefficients = tf.reshape(scattering_coefficients, [batch_size, -1])
    dimensions = scattering_coefficients.get_shape().as_list()[1:]
    scattering_coefficients = tf.reshape(scattering_coefficients, [-1, np.prod(dimensions)])
    print(scattering_coefficients)
    n_classes = 10
    n_coefficients = scattering_coefficients.get_shape().as_list()[1]

    # use linear classifier
    W = tf.Variable(tf.zeros([n_coefficients, n_classes]))
    b = tf.Variable(tf.zeros([n_classes]))
    y_predict = tf.nn.softmax(tf.matmul(scattering_coefficients, W) + b)

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions={"prediction": y_predict})

    # loss function and training step
    cross_entropy = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(labels=labels, logits=y_predict) )
    train_op = tf.train.GradientDescentOptimizer(params["learning_rate"]).minimize(
        cross_entropy, global_step=tf.train.get_global_step())

    # train_op = tf.train.GradientDescentOptimizer(learning_rate=params["learning_rate"]).minimize(
    #     loss=loss)

    return tf.estimator.EstimatorSpec(
        mode=mode,
        loss=cross_entropy,
        train_op=train_op)



if __name__ == '__main__':
