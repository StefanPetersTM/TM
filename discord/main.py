from discord.ext import commands
import discord

import os
import sys
import random
import json

import chat
import encoder
import model
import numpy as np
import sample
import tensorflow as tf


def session():
    # Hyperparameters
    model_name = 'E:\\Programs\\PyCharmCommunityEdition2019.1.3\\PycharmProjects\\NexthinkChatbotPrototype\\models\\774M'
    seed = None
    length = 20
    temperature = .9
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

    sess = tf.Session()
    np.random.seed(seed)
    tf.set_random_seed(seed)
    context = tf.placeholder(tf.int32, [1, None])
    output = sample.sample_sequence(
        hparams=hparams, length=length,
        context=context,
        batch_size=1,
        temperature=temperature, top_k=top_k
    )

    saver = tf.train.Saver()
    ckpt = tf.train.latest_checkpoint(os.path.join('models', model_name))
    saver.restore(sess, ckpt)
    print("\nUsing checkpoint from:\n" + ckpt)
    return enc, sess, output, context, bot_name


description = '''List of all commands'''
bot = commands.Bot(command_prefix='!', description=description)


@bot.event
async def on_ready():
    print('\nLogged in as')
    print(bot.user.name)
    print('------')
    print("\nEverything's up and running chief.")
    await bot.change_presence(activity=discord.Game(name='!!! for new conv'))

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@bot.command(description='Restart conversation')
async def clear(ctx):
    """Clear the current conversation"""
    await ctx.channel.send('Clearing messages...', delete_after=2)
    await ctx.channel.send("New conversation from here on:")
    # async for msg in client.logs_from(message.channel):
    #   if not msg.pinned:
    #        await bot.delete_message(msg)
    # messages = []
    for i in bot.cached_messages._SequenceProxy__proxied:
        await i.delete()
    return

@bot.command()
async def ping(ctx):
    """simple ping test tool"""
    await ctx.send(f'Pong! {round(bot.latency*1000)}ms')

@bot.command()
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguments")
    else:
        print("Command error: " + error)
        await ctx.send("Command error: " + error)

@bot.event
async def on_message(message):
    if "!" not in message.content[0]:
        conversation = """{0}: hi. what's your name?
{1}: {1}. and you?
{0}: I'm {0}
{1}: so what can I do for you?
""".format(message.author.display_name, bot_name)

        for i in bot.cached_messages._SequenceProxy__proxied:
            if "!" not in i.content[0] and i.tts == True:
                if str(i.author) == "BotMcBotty#3002":
                    conversation = conversation + (i.content + "\n")
                else:
                    conversation = conversation + (
                            "{}: ".format(message.author.display_name) + i.content + "\n{}: ".format(bot_name))

        if str(message.author) == "BotMcBotty#3002":
            print("\nBot message duplicate")
        else:
            if message.content == "!!!":
                conversation = None

            if message.content == "///":
                await message.channel.send("Restarting bot")
                python = sys.executable
                os.execl(python, python, *sys.argv)

            conversation = conversation + ("\n{}: ".format(message.author.display_name))
            reply, conversations = chat.get_reply(enc, sess, output, context, message.content, message.author.display_name, bot_name, conversation)

            conversation = conversation + reply
            print("\n\n\nCURRENT CONVERSATION with {}:\n".format(message.author.display_name) + conversation)
            await message.channel.send(reply, tts=True)
    await bot.process_commands(message)

enc, sess, output, context, bot_name = session()
bot.run('NjE4ODU3MzAxMTM4MjEwODQ2.XXF4uA.boORRlDN7JvN76Cpvqp62MWNipY')
