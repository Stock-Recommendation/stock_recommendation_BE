from datasets import load_dataset
from transformers import RobertaTokenizer, FlaxRobertaForSequenceClassification, AutoConfig
from flax.training.common_utils import get_metrics, onehot, shard, shard_prng_key
import jax.numpy as jnp
import numpy as np
import jax

def train_data_loader(rng, dataset, batch_size):
    steps_per_epoch = len(dataset) // batch_size
    perms = jax.random.permutation(rng, len(dataset)) #shuffle
    perms = perms[: steps_per_epoch * batch_size]  # Skip incomplete batch.
    perms = perms.reshape((steps_per_epoch, batch_size))
    for perm in perms:
        batch = dataset[perm]
        batch = {k: jnp.array(v) for k, v in batch.items()}
        batch = shard(batch)
        yield batch

def eval_data_loader(dataset, batch_size):
    for i in range(len(dataset) // batch_size):
        batch = dataset[i * batch_size : (i + 1) * batch_size]
        batch = {k: jnp.array(v) for k, v in batch.items()}
        batch = shard(batch)
        yield batch

def sentiment140_ds():
    dataset = 'sentiment140'
    model_name = "roberta-base"
    raw_ds = load_dataset(dataset)
    print(raw_ds)
    sorted_dataset = raw_ds.sort("sentiment")
    shuffled_dataset = sorted_dataset.shuffle(seed=42)

    shuffled_ds = shuffled_dataset['train'].train_test_split(test_size=0.05)

    raw_ds_test = shuffled_ds['test']
    raw_ds_train = shuffled_ds['train']

    tokenizer = RobertaTokenizer.from_pretrained(model_name)

    def prepocess_fn(examples):
        texts = ((examples['text'],))

        processed = tokenizer(*texts,
                              max_length=128,
                              truncation=True,
                              padding="max_length")
        lst = examples["sentiment"]
        for i in range(len(lst)):
            if lst[i] == 0:
                lst[i] = 0
            elif lst[i] == 4:
                lst[i] = 1
        processed["label"] = np.array(lst)
        return processed

    ds_test = raw_ds_test.map(prepocess_fn, batched=True, remove_columns=['text', 'date', 'user', 'sentiment', 'query'])
    ds_train = raw_ds_train.map(prepocess_fn, batched=True, remove_columns=['text', 'date', 'user', 'sentiment', 'query'])

    return ds_train, ds_test, model_name, tokenizer