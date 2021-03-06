#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------
# File:    train.py
# Author:  Michael Gharbi <gharbi@mit.edu>
# Created: 2016-10-25
# -------------------------------------------------------------------
#
#
#
# ------------------------------------------------------------------#
"""Train a model."""

import argparse
import os
import time

import numpy as np
import tensorflow as tf
import setproctitle

import quakenet.models as models
import quakenet.data_pipeline as dp
import quakenet.config as config


def main(args):
  setproctitle.setproctitle('quakenet')

  tf.set_random_seed(1234)

  if args.n_clusters == None:
    raise ValueError('Define the number of clusters with --n_clusters')

  cfg = config.Config()
  cfg.batch_size = args.batch_size
  cfg.add = 1
  cfg.n_clusters = args.n_clusters
  cfg.n_clusters += 1

  pos_path = os.path.join(args.dataset,"positive")
  neg_path = os.path.join(args.dataset,"negative")

  # data pipeline for positive and negative examples
  pos_pipeline = dp.DataPipeline(pos_path, cfg, True)
  neg_pipeline = dp.DataPipeline(neg_path, cfg, True)

  pos_samples = {
    'data': pos_pipeline.samples,
    'cluster_id': pos_pipeline.labels
    }
  neg_samples = {
    'data': neg_pipeline.samples,
    'cluster_id': neg_pipeline.labels
    }

  samples = {
   "data": tf.concat(0,[pos_samples["data"],neg_samples["data"]]),
   "cluster_id" : tf.concat(0,[pos_samples["cluster_id"],neg_samples["cluster_id"]])
  }

  # model
  model = models.get(args.model, samples,cfg, args.checkpoint_dir, is_training=True)

  # train loop
  model.train(
    args.learning_rate,
    resume=args.resume,
    profiling=args.profiling,
    summary_step=10)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--model', type=str, default='ConvNetQuake')
  parser.add_argument('--checkpoint_dir', type=str, default='output/checkpoints')
  parser.add_argument('--dataset', type=str, default='data/hackathon/train')
  parser.add_argument('--batch_size', type=int, default=64)
  parser.add_argument('--learning_rate', type=float, default=1e-4)
  parser.add_argument('--gpu', type=int, default=0)
  parser.add_argument('--resume', action='store_true')
  parser.set_defaults(resume=False)
  parser.add_argument('--profiling', action='store_true')
  parser.add_argument('--n_clusters',type=int,default=None)
  parser.set_defaults(profiling=False)
  args = parser.parse_args()

  os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)
  args.checkpoint_dir = os.path.join(args.checkpoint_dir, args.model)

  main(args)
