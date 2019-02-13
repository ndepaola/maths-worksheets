import asyncio
import config
from discord.ext import commands
from bot_functions import *

client = discord.Client()

# Commands
bot = commands.Bot(command_prefix='.')


@bot.command()
async def add(ctx, *, text: str = None):
    """
    Add a topic to a student.
    usage: .add <topic> to <student>
    input: <topic>: The topic you want to add, case sensitive.
    input: <student>: The student's full name.
    output: The bot will tell you if it was successful or not.
    """
    if text is None:
        await ctx.channel.send('Sorry, I couldn\'t find a command here.')
    else:
        async with ctx.channel.typing():
            await ctx.channel.send(embed=add_topics_to_student(
                text=text,
                author=ctx.message.author.id
            ))


@bot.command()
async def remove(ctx, *, text: str = None):
    """
    Remove a topic from a student.
    usage: .remove <topic> from <student>
    input: <topic>: The topic you want to remove, case sensitive.
    input: <student>: The student's full name.
    output: The bot will tell you if it was successful or not.
    """
    if text is None:
        await ctx.channel.send('Sorry, I couldn\'t find a command here.')
    else:
        async with ctx.channel.typing():
            await ctx.channel.send(embed=remove_topics_from_student(
                text=text,
                author=ctx.message.author.id
            ))


@bot.command()
async def list(ctx, *, text: str):
    """
    List various things.
    usage: .list all curricula
    output: A list of all curricula (modules containing topis) currently available.

    usage: .list my students
    output: Each student currently registered as yours.

    usage: .list all topics
    output: All topics currently available, and what curricula they originate from.

    usage: .list topics in <curricula>
    output: All topics currently available in a specified curricula.
    """
    if 'all curricula' in text:
        await ctx.channel.send(get_all_curricula(ctx.message))

    # X (student name)
    elif 'my students' in text:
        async with ctx.channel.typing():
            embeds = print_all_students(ctx.message)
            for embed in embeds:
                await ctx.channel.send(embed=embed)

    elif 'all topics' in text:
        await ctx.channel.send(get_all_topics(ctx.message))

    elif 'topics in' in text:
        await ctx.channel.send(get_topics_in_curriculum(ctx.message))


@bot.command()
async def delete(ctx, *, student_name: str = None):
    """
    Delete a student from the database.
    usage: .delete <student>
    input: <student>: the student's full name.
    output: The bot will tell you if it was successful or not.
    """
    if student_name is None:
        await ctx.channel.send('Sorry, I couldn\'t find a command here.')
    else:
        async with ctx.channel.typing():
            await ctx.channel.send(embed=delete_student(
                student_name=student_name,
                author=ctx.message.author.id))


@bot.command()
async def get(ctx, *, text: str = None):
    """
    Generate a LaTeX doc with questions and answers.
    usage: .get <type> <student>
    input: <type>: sheet (only option currently with more on the horizon)
    input: <student>: the student's full name.
    output: The bot will upload PDFs of the questions and answers.
    """
    if text is None:
        await ctx.channel.send('Sorry, I couldn\'t find a command here.')
    else:
        # Generate worksheet
        # Generate practice exam?
        # Generate real exam?
        if 'sheet' in text:
            student_name = re.findall(r'(?<=sheet )(.*\n?)', text)[0]
            async with ctx.channel.typing():
                # Generate worksheet for the specified student
                tup = get_worksheet(
                    student_name=student_name,
                    author=ctx.message.author.id)
                await ctx.channel.send(embed=tup[0])
                try:
                    with open(tup[1], 'rb') as fp1, open(tup[2], 'rb') as fp2:
                        await ctx.channel.send(file=discord.File(fp=fp1))
                        await ctx.channel.send(file=discord.File(fp=fp2))
                except FileNotFoundError:
                    print('Couldn\'t find the requested files to send.')


@bot.command()
async def create(ctx, *, text: str = None):
    """
    Create a student and add it to the database.
    usage: enter your student's information like shown below.

    .create
    firstname: <student's first name>
    lastname: <student's last name>
    address: <student's address>
    grade: <student's grade>
    contactnumber: <student/parent/guardian\s phone number>

    output: The bot will tell you if it was successful or not.
    """
    async with ctx.channel.typing():
        await ctx.channel.send(embed=create_student(
            text=text,
            author=ctx.message.author.id))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    # prepare_database()
    add_students()

# Run the bot
bot.run(config.TOKEN)
