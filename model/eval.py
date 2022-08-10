import jax
from finetune import *

roberta_apply_repl = jax.pmap(lambda params, inputs: state.apply_fn(**inputs, params=params, train=False))

def get_accuracy(params_repl):
  good = total = 0
  steps = len(ds_test)//128
  for _, batch in zip(tqdm.trange(steps), eval_data_loader(ds_test, 128)):
    labels = batch.pop('label')
    labels = jax.nn.one_hot(labels, num_classes=2)
    predicted = roberta_apply_repl(params_repl, batch)[0]
    is_same = predicted.argmax(axis=-1) == labels.argmax(axis=-1)
    good += is_same.sum()
    total += len(is_same.flatten())
  return good / total

print(get_accuracy(state.params))