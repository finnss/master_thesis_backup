import tensorflow as tf
from stable_baselines import TD3
import time
from tensorflow.python.tools import freeze_graph

saved_model_dir = "../trained_models/agent.zip"

model = TD3.load(saved_model_dir)
gdef = model.graph
tf.train.write_graph(gdef, ".", "saved_model.pb", False)

"""
init = tf.global_variables_initializer()
# sess.run(init)
saver = tf.train.Saver()
saver.save(sess, './tensorflowModel.ckpt')



freeze_graph.freeze_graph('graph.pb', "", False,
                          './tensorflowModel.ckpt', "output/softmax",
                          "save/restore_all", "save/Const:0",
                          'frozentensorflowModel.pb', True, ""
                          )
converter = tf.lite.TFLiteConverter.from_session(
    model.sess, [model.observations_ph], [model.policy_out])

"""
converter = tf.lite.TFLiteConverter.from_saved_model('./')

tflite_model = converter.convert()
open("test.tflite", "wb").write(tflite_model)
