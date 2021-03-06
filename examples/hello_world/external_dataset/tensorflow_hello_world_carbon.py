#  Copyright (c) 2018-2019 Huawei Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Minimal example of how to read samples from a dataset generated by `generate_external_dataset_carbon.py`
using tensorflow, using make_batch_carbon_reader() instead of make_carbon_reader()"""

from __future__ import print_function

import argparse
import jnius_config

import tensorflow as tf

from pycarbon.carbon_tf_utils import tf_tensors, make_pycarbon_dataset

from pycarbon.carbon_reader import make_batch_carbon_reader

from examples import DEFAULT_CARBONSDK_PATH


def tensorflow_hello_world(dataset_url='file:///tmp/carbon_external_dataset'):
  # Example: tf_tensors will return tensors with dataset data
  with make_batch_carbon_reader(dataset_url) as reader:
    tensor = tf_tensors(reader)
    with tf.Session() as sess:
      # Because we are using make_batch_reader(), each read returns a batch of rows instead of a single row
      batched_sample = sess.run(tensor)
      print("id batch: {0}".format(batched_sample.id))

  # Example: use tf.data.Dataset API
  with make_batch_carbon_reader(dataset_url) as reader:
    dataset = make_pycarbon_dataset(reader)
    iterator = dataset.make_one_shot_iterator()
    tensor = iterator.get_next()
    with tf.Session() as sess:
      batched_sample = sess.run(tensor)
      print("id batch: {0}".format(batched_sample.id))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Tensorflow hello world')
  parser.add_argument('-c', '--carbon-sdk-path', type=str, default=DEFAULT_CARBONSDK_PATH,
                      help='carbon sdk path')

  args = parser.parse_args()

  jnius_config.set_classpath(args.carbon_sdk_path)

  tensorflow_hello_world()
