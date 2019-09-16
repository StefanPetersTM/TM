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
from urllib.request import Request, urlopen


def session():
    # Hyperparameters
    model_name = 'E:\\Programs\\PyCharmCommunityEdition2019.1.3\\PycharmProjects\\NexthinkChatbotPrototype\\models\\774M'
    seed = None
    length = 50
    temperature = 0.85
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

bot = commands.Bot(command_prefix='!', description='''List of all commands''')


@bot.event
async def on_ready():
    print('\nLogged in as')
    print(bot.user.name)
    print('------')
    print("\nEverything's up and running chief.")
    await bot.change_presence(activity=discord.Game(name='Use at your own risk'))

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

@bot.command()
async def bug(message):
    """Take a bug report"""
    await message.channel.send("Please fill out this form to report a bug: https://forms.gle/FyeWKuGdzu5wfyUL6")

@bot.command(description='Restart conversation')
async def clear(message):
    """Clear the current conversation"""
    await message.channel.send('Clearing messages...', delete_after=2)
    await message.channel.send("New conversation from here on:")
    # async for msg in client.logs_from(message.channel):
    #   if not msg.pinned:
    #        await bot.delete_message(msg)
    # messages = []
    async for msg in bot.cached_messages._SequenceProxy__proxied(message.channel):
        if not msg.pinned:
            await bot.delete_message(msg)

    #for i in bot.cached_messages._SequenceProxy__proxied:
    #    await i.delete()
    return

@bot.event
async def on_message(message):
    if not message.attachments and "!" not in message.content[0] and str(message.author) != "BotMcBotty#3002" and "```" not in message.content:
        conversation = """{0}: hi. what's your name?
{1}: {1}. and you?
{0}: I'm {0}
{1}: so what can I do for you?
""".format(message.author.display_name, bot_name)

        for i in bot.cached_messages._SequenceProxy__proxied:
            if "!" not in i.content[0] and "!help" not in i.content:
                if str(i.author) == "BotMcBotty#3002" and "```" not in message.clean_content:
                    conversation = conversation + (i.content + "\n")
                elif "```" not in message.clean_content:
                    conversation = conversation + (
                            "{}: ".format(message.author.display_name) + i.content + "\n{}: ".format(bot_name))

        if str(message.author) == "BotMcBotty#3002":
            print("\nBot message duplicate")
        else:
            if message.content == ";;;":
                conversation = None

            if message.content == "///":
                await message.channel.send("Restarting bot. Please wait for ~30s.")
                python = sys.executable
                os.execl(python, python, *sys.argv)

            reply, conversations = chat.get_reply(enc, sess, output, context, message.content, message.author.display_name, bot_name, conversation)

            conversation = conversation + reply
            print("\n\n\nCURRENT CONVERSATION with {}:\n".format(message.author.display_name) + conversation)
            await message.channel.send(reply, tts=True)
    elif message.attachments and str(message.author) != "BotMcBotty#3002":
        print("Image sent to bot: " + str(message.attachments))
        req = Request(message.attachments[0].url, headers={'User-Agent': 'Mozilla/5.0'})
        img = urlopen(req).read()

        fhand = open('discord.jpg', 'wb')
        fhand.write(img)
        fhand.close()

        fhand = open('discord.jpg', 'rb')
        await message.channel.send(file=discord.File(fhand, 'image_echo.png'))
    elif str(message.author) != "BotMcBotty#3002":
        await bot.process_commands(message)

enc, sess, output, context, bot_name = session()
bot.run('NjE4ODU3MzAxMTM4MjEwODQ2.XX62iA.yspNlB48y3bOCMCme_noLtMDgdc')
