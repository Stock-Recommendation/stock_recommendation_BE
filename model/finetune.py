import jax
import flax
import optax
import tqdm
import jax.numpy as jnp
from preprocess import *
import matplotlib.pyplot as plt
from flax.training import train_state, checkpoints
from flax.training.common_utils import get_metrics, onehot, shard, shard_prng_key

def make_update_fn(lr_fn):
  def train_step(state, batch, dropout_rng):
      labels = batch.pop("label")
      dropout_rng, new_dropout_rng = jax.random.split(dropout_rng)

      def cross_entropy_loss(logits, labels):
          xentropy = optax.softmax_cross_entropy(logits, onehot(labels, num_classes=2))
          return jnp.mean(xentropy)

      def loss_fn(params):
          logits = state.apply_fn(**batch, params=params, dropout_rng=dropout_rng, train=True)[0]
          loss = cross_entropy_loss(logits, labels)
          return loss

      grad_fn = jax.value_and_grad(loss_fn)
      loss, grads = grad_fn(state.params)
      grads = jax.lax.pmean(grads, "batch")
      new_state = state.apply_gradients(grads=grads)
      metrics = jax.lax.pmean({"loss": loss, "lr": lr_fn(state.step)}, axis_name="batch")
      return new_state, metrics, new_dropout_rng

  return jax.pmap(train_step, axis_name='batch', donate_argnums=(0,))

def train(model, batch_size, base_lr, ds_train, steps):

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

    update_fn_repl = make_update_fn(lr_fn=lr_schedule)

    rng = jax.random.PRNGKey(42)
    dropout_rngs = jax.random.split(rng, jax.local_device_count())
    state = flax.jax_utils.replicate(state)

    losses = []

    for step, batch in zip(tqdm.trange(1, steps+1), train_data_loader(rng, ds_train, batch_size)):

      state, metrics, dropout_rngs = update_fn_repl(state, batch, dropout_rngs)
      loss = flax.jax_utils.unreplicate(metrics)['loss'].item()
      losses.append(loss)
      if step == 1 or step % 500 == 0:
        print("loss: {}".format(loss))

    plt.plot(losses)

    return state

steps = 11_875
base_lr = 4e-5
batch_size = 128

ds_train, ds_test, model_name, tokenizer = sentiment140_ds()
config = AutoConfig.from_pretrained(model_name, num_labels=2)
model = FlaxRobertaForSequenceClassification.from_pretrained(model_name, config=config, seed=0)

state = train(model=model, batch_size=batch_size, base_lr=base_lr, ds_train=ds_train, steps=steps)

checkpoints.save_checkpoint(ckpt_dir="save/ckpt", target=flax.jax_utils.unreplicate(state), step=steps)
tokenizer.save_pretrained("save/tokenizer")


