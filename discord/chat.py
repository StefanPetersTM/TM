# Use the commented code below to run a session
# Use the function below to get a reply from gpt2

# Define function that gets called everytime to get a reply
import os
import tensorflow as tf
import json
import numpy as np

import encoder
import model
import sample

def session():
    # Hyperparameters
    model_name = r'D:\GithubProjects\TM\774M'
    seed = None
    length = 50
    temperature = 0.9
    top_k = 0

    global bot_name
    bot_name = "Bot"

    # Open session and maintain it
    enc = encoder.get_encoder(model_name)
    hparams = model.default_hparams()
    with open(os.path.join('models', model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    sess1 = tf.Session()

    np.random.seed(seed)
    tf.set_random_seed(seed)
    context = tf.placeholder(tf.int32, [1, None])
    output = sample.sample_sequence(
        hparams=hparams, length=length,
        context=context,
        batch_size=1,
        temperature=temperature, top_k=top_k
    )

    saver1 = tf.train.Saver()
    ckpt = tf.train.latest_checkpoint(os.path.join('models', model_name))
    saver1.restore(sess1, ckpt)

    print("\nUsing checkpoint from:\n" + ckpt)
    return enc, sess1, output, context, bot_name

def get_reply(
        enc,
        sess1,
        output,
        context,

        message,
        user_name,
        bot_name,
        conversation
):
    if conversation == None:
        conversation = """{0}: hi. what's your name?
{1}: {1}. and you?
{0}: I'm {0}
{1}: so what can I do for you?
{0}: """.format(user_name, bot_name)

    encoded_conversation = enc.encode(conversation)
    result = sess1.run(output, feed_dict={
        context: [encoded_conversation]
    })[:, len(encoded_conversation):]
    text = enc.decode(result[0])
    splits = text.split('\n')
    reply = splits[0]
    conversation = conversation + (reply)
    # print("\nBot:"+reply)

    return reply, conversation
