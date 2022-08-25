from transformers import AutoTokenizer, FlaxRobertaForSequenceClassification, AutoConfig
from flax.training import train_state, checkpoints
import jax.numpy as jnp
import jax
import flax
import optax
from model.preprocess import *


config = AutoConfig.from_pretrained("roberta-base", num_labels=2)
model = FlaxRobertaForSequenceClassification.from_pretrained("roberta-base", config=config, seed=0)

steps = 11_875
base_lr = 4e-5

lr_schedule = optax.cosine_decay_schedule(init_value=-base_lr, decay_steps=steps)

gradient_transform = optax.chain(
    optax.clip_by_global_norm(1.0),
    optax.scale_by_adam(),
    optax.scale_by_schedule(lr_schedule),
)

state = train_state.TrainState.create(
    apply_fn=model.__call__,
    params=model.params,
    tx=gradient_transform,
)

restored_tokenizer = AutoTokenizer.from_pretrained("/Users/dttai11/RoBERTa/save/tokenizer")

restored_state = checkpoints.restore_checkpoint(ckpt_dir="/Users/dttai11/RoBERTa/save/ckpt", target=state)

devices = jax.local_devices() #8
restored_params = jax.device_put_replicated(restored_state.params, devices)

tweets = ["is slowly realizing the fact that her momz is moving to Europe to join Dad tmrw and she'll be living alone..getting abit sad. ",
          "it's the chack it out week  In this week, i will write 'check it out' in all my uptades here in twitter, haha",
          'The computers and the Ethernet at school are so slow! ',
          'grillen with the fam... SO HAPPY  one one person missing... YOU!!! (stop by if your close by )',
          "@smugfuzz I didn't realise you were such a patriot ",
          "@KrackofDawn oh no I'm sorry!  warning:  I'm going to wec tonight and will prob be tweeting...",
          'My mouth hurts!!! ',
          'curiosity killed the cat. fortunately, cats have 9 lives. '] #input tweets here
lst = []

for tweet in tweets:
  encoded_tweet = restored_tokenizer.encode(tweet, max_length=32, truncation=True, padding="max_length")
  lst.append(jnp.array(encoded_tweet))

input_ids = jnp.array(lst)

features = model(input_ids, params = flax.jax_utils.unreplicate(restored_params))[0]

print(jax.nn.softmax(features))
print(features.argmax(axis=-1))