# Use the commented code below to run a session
# Use the function below to get a reply from gpt2

#Define function that gets called everytime to get a reply
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

    #    conversation = conversation + (str(message))
    #conversation = conversation + ("{}: ".format(bot_name))



    encoded_conversation = enc.encode(conversation)
    result = sess1.run(output, feed_dict={
        context: [encoded_conversation]
    })[:, len(encoded_conversation):]
    text = enc.decode(result[0])
    splits = text.split('\n')
    reply = splits[0]
    conversation = conversation + (reply)
    #print("\nBot:"+reply)

    return reply, conversation
