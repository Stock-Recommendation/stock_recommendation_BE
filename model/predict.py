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

restored_tokenizer = AutoTokenizer.from_pretrained("save/tokenizer")

restored_state = checkpoints.restore_checkpoint(ckpt_dir="save/ckpt", target=state)

devices = jax.local_devices() #8
restored_params = jax.device_put_replicated(restored_state.params, 8)

tweets = [] #input tweets here
lst = []

for tweet in tweets:
  encoded_tweet = restored_tokenizer.encode(tweet, max_length=32, truncation=True, padding="max_length")
  lst.append(jnp.array(encoded_tweet))

input_ids = jnp.array(lst)

features = model(input_ids, params = flax.jax_utils.unreplicate(restored_params))[0]

print(jax.nn.softmax(features))
print(features.argmax(axis=-1))