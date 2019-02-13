from generate_sheet import *
import sys, inspect
import pyclbr
import re
import sqlite3
import discord

student_list = []


class Student:
    firstName = ""
    lastName = ""
    address = ''
    grade = ''
    creator_discord_id = ''
    topic_list = []
    contact_number = ''  # phone number of student or parent
    db_id = 0

    def add_topic(self, topic):
        if self.topic_list == "None":
            self.topic_list = []
        if topic not in self.topic_list:
            self.topic_list.append(topic)
            return True
        else:
            return False

    def remove_topic(self, topic):
        if topic in self.topic_list:
            self.topic_list = [y for y in self.topic_list if y != topic]
            return True
        else:
            return False

    def list_topics(self):
        topics = ""
        if self.topic_list and self.topic_list != "None":
            for topic in self.topic_list:
                topics += topic.name + ", "
            topics = topics[0:-2]
        else:
            topics = "None"
        return topics

    def __str__(self):
        return self.firstName + " " + self.lastName

    def __init__(self, firstName, lastName, grade, address,
                 discord_id, contact_number, topic_list=[], db_id=0):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.grade = grade
        self.creator_discord_id = discord_id
        self.contact_number = contact_number
        self.topic_list = topic_list
        self.db_id = db_id

    def get_info(self):
        print("Str:")
        print(str(self))
        print("Got called")

        # Generate info suitable to pass to the generate_sheet function
        topics = []
        for topic in self.topic_list:
            if topic not in topics:
                topics.append( (str_to_class(topic.name), str_to_class(topic.name).default_num() ) )

        info = {
            "name": str(self),
            "grade": self.grade,
            "topics": topics,
        }

        return info


def print_all_students(message):
    embeds = []
    print(student_list)
    print(type(message.author.id))
    if student_list:
        for student in student_list:
            if student.creator_discord_id == str(message.author.id) or message.author.id == 273256425663234050:
                embed = discord.Embed(title=str(student), color=0x00ff00)
                embed.add_field(name="Address", value=student.address, inline=False)
                embed.add_field(name="Phone Number", value=student.contact_number, inline=True)
                embed.add_field(name="Year Level", value=student.grade, inline=True)
                embed.add_field(name="db ID", value=student.db_id, inline=True)
                embed.add_field(name="Topic List", value=student.list_topics(), inline=True)
                embed.add_field(name="Tutor", value="<@%s>" % student.creator_discord_id , inline=True)
                embeds.append(embed)
        return embeds
    else:
        embed = discord.Embed(title="No Students",
                              description="Looks like you don't have any students yet.",
                              color=0xff0000)
        return embed


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


def get_worksheet(student_name, author):
    print(student_name)
    # Generate a worksheet for the current student
    # student_name = re.findall(r'(?<= get sheet for )(.*\n?)', message.content)[0]

    # Locate student
    student = get_student(student_name, str(author))
    if student:
        # Make sure there are any topics in the student
        if student.topic_list and student.topic_list != "None":
            # Generate the worksheets
            out_paths = generate_sheet(student.get_info())

            # Attach and send
            msg = "Here are the files for the worksheet you requested for %s:" % student_name
            embed = discord.Embed(title="Worksheet for %s" % str(student),
                                  description=msg,
                                  color=0x00ff00)

            out = (embed, out_paths[0], out_paths[1])
        else:
            msg = "Sorry, it seems like your student doesn't have any topics currently."
            embed = discord.Embed(title="Failed to Generate Worksheet",
                                  description=msg,
                                  color=0xff0000)
            out = (embed, "", "")
    else:
        msg = "Sorry, I couldn't locate that student in the database."
        embed = discord.Embed(title="Failed to Generate Worksheet",
                              description=msg,
                              color=0xff0000)
        out = (embed, "", "")
    return out


def print_classes():
    output = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            output.append(obj)
    return output


def get_all_curricula(message):
    msg = ''
    module_name = 'generate_sheet'
    module_info = pyclbr.readmodule(module_name)
    for item in module_info.values():
        if 'default_num' in item.methods and item.module not in msg:
            msg += (item.module + ', ')
    msg = msg[:-2]
    return msg


def get_all_topics(message):
    msg = ''
    module_name = 'generate_sheet'
    module_info = pyclbr.readmodule(module_name)
    for item in module_info.values():
        # Check if item has attribute "insert_question"
        if 'default_num' in item.methods:
            msg += (item.name + ', in ' + item.module + '\n')
    return msg


def get_topics_in_curriculum(message):
    topic = message.content.replace('.list topics in ', '')
    try:
        msg = ''
        module_info = pyclbr.readmodule(topic)
        for item in module_info.values():
            # Check if item has attribute "insert_question"
            if 'default_num' in item.methods:
                msg += (item.name + '\n')

    except AttributeError:
        # User misspelled a module, so spit back an error
        msg = "Sorry, I couldn't find that module."

    return msg


def get_student(student_name, id):
    for student in student_list:
        if student.creator_discord_id in id and str(student) == student_name:
            return student
    return False


def create_student(text, author):
    first_name = re.findall(r'firstname: (.*?)\n', text)
    last_name = re.findall(r'lastname: (.*?)\n', text)
    grade = re.findall(r'grade: (.*?)\n', text)
    address = re.findall(r'address: (.*?)\n', text)
    contact_number = re.findall(r'contactnumber: (.*?)$', text)

    # Validate that this tutor doesn't currently have a client with the same name
    if get_student(first_name[0] + " " + last_name[0], str(author)):
        # Student exists, so stop here
        embed = discord.Embed(title="Failed to Add Student",
                              description="You already have a student with the same name.",
                              color=0xFF0000)
        return embed

    student_list.append(Student(
        firstName=first_name[0],
        lastName=last_name[0],
        grade=str(grade[0]),
        contact_number=str(contact_number[0]),
        address=address[0],
        discord_id=str(author)))

    # insert into database
    new_id = create_student_db(student_list[-1])
    student_list[-1].db_id = new_id

    # return a nice embed to let the user know we did the thing
    embed = discord.Embed(title="New Student",
                          description="I've added this student to the database for you.", color=0x00ff00)
    embed.add_field(name="Name", value=str(student_list[-1]), inline=True)
    embed.add_field(name="Address", value=student_list[-1].address, inline=True)
    embed.add_field(name="Phone Number", value=student_list[-1].contact_number, inline=True)
    embed.add_field(name="Year Level", value=student_list[-1].grade, inline=True)
    embed.add_field(name="db ID", value=str(student_list[-1].db_id), inline=True)
    embed.add_field(name="Topic List", value=student_list[-1].list_topics(), inline=False)

    return embed


def delete_student(student_name, author):
    print(student_name)
    student = get_student(student_name=student_name, id=str(author))
    if student:
        # Located our student
        delete_student_db(student=student)

        # Fancy looking embed
        embed = discord.Embed(title="Deleted Student",
                              description="I've deleted %s from the database for you." % student_name,
                              color=0x00ff00)

        # Remove from list, then delete the student object
        student_list.remove(student)
        del student
    else:
        # Fancy looking embed
        embed = discord.Embed(title="Couldn't Delete Student",
                              description="I couldn't find %s in the database." % student_name,
                              color=0xff0000)
    return embed


def add_topics_to_student(text, author):
    msg_yes = "Successfully added "
    msg_no = "Failed to add "
    succeeded = False
    failed = False

    # Parse inputs
    req_topics = re.findall(r'^(.*\n?)(?= to )', text)[0]
    student_name = re.findall(r'(?<= to )(.*\n?)', text)[0]
    topic_list = req_topics.split(', ')

    # Loop over all students to locate our student
    student = get_student(student_name=student_name, id=str(author))
    if student:
        # Located our student
        module_name = 'generate_sheet'
        module_info = pyclbr.readmodule(module_name)
        # Loop over all available topics and see which ones the user requested
        for item in module_info.values():
            if item.name in topic_list:
                # User requested to add this topic - try to do it
                if item.name not in student.list_topics():
                    student.add_topic(item)
                    msg_yes += item.name + ", "
                    if not succeeded:
                        succeeded = True

                else:
                    msg_no += item.name + ", "
                    if not failed:
                        failed = True

    # Format the output message
    msg = "For student %s: \n" % student_name
    if succeeded:
        msg += msg_yes[:-2] + ". \n"
        update_student_db(student)

    if failed:
        msg += msg_no[:-2] + ". This student already has this topic(s). \n"
    embed = discord.Embed(title="Topic Add Results", description=msg, color=0x00ff00)
    return embed


def remove_topics_from_student(text, author):
    msg_yes = "Successfully removed "
    msg_no = "Failed to remove "
    succeeded = False
    failed = False

    # Parse inputs
    req_topics = re.findall(r'^(.*\n?)(?= from )', text)[0]
    student_name = re.findall(r'(?<= from )(.*\n?)', text)[0]
    topic_list = req_topics.split(', ')

    # Loop over all students to locate our student
    student = get_student(student_name=student_name, id=str(author))
    if student:
        # Located our student
        module_name = 'generate_sheet'
        module_info = pyclbr.readmodule(module_name)
        # Loop over all available topics and see which ones the user requested
        for item in module_info.values():
            if item.name in topic_list:
                # User requested to remove this topic - try to do it
                if item.name in student.list_topics():
                    student.remove_topic(item)
                    msg_yes += item.name + ", "
                    if not succeeded:
                        succeeded = True

                else:
                    msg_no += item.name + ", "
                    if not failed:
                        failed = True

    # Format the output message
    msg = "For student %s: \n" % student_name
    if succeeded:
        msg += msg_yes[:-2] + ". \n"
        update_student_db(student)

    if failed:
        msg += msg_no[:-2] + ". This student doesn't have this topic(s). \n"
    embed = discord.Embed(title="Topic Removal Results", description=msg, color=0x00ff00)
    return embed


def update_student_db(student):
    update_command = """UPDATE student 
                        SET topic_list = ? 
                        WHERE student_id = ? """
    data = (student.list_topics(), student.db_id)
    execute_sql(command=update_command, data=data)


def delete_student_db(student):
    delete_command = """DELETE FROM student
                        WHERE student_id = ? """
    data = [(student.db_id)]
    execute_sql(command=delete_command, data=data)


def create_student_db(student):
    format_command = """
    INSERT INTO student (
    student_id, first_name, last_name, address, 
    grade, creator_id, topic_list, contact_number)
    VALUES (NULL, "{first}", "{last}", "{address}", "{grade}", 
            "{creator_id}", "{topic_list}", "{contact_number}");"""

    update_command = format_command.format(
        first=student.firstName,
        last=student.lastName,
        address=student.address,
        grade=student.grade,
        creator_id=student.creator_discord_id,
        topic_list=student.list_topics(),
        contact_number=student.contact_number)
    return execute_sql(update_command)


def execute_sql(command, data=()):
    # Prepare database
    connection = sqlite3.connect("company.db")
    cursor = connection.cursor()
    cursor.execute(command, data)
    last_id = cursor.lastrowid
    # Commit and close
    connection.commit()
    connection.close()
    return last_id


def prepare_database():
    init_command = """
            CREATE TABLE student (
            student_id INTEGER PRIMARY KEY,
            first_name VARCHAR(20),
            last_name VARCHAR(20),
            address VARCHAR(80),
            grade VARCHAR(4),
            creator_id VARCHAR(20),
            topic_list VARCHAR(200),
            contact_number VARCHAR(20));"""
    execute_sql(command=init_command)


def add_students():
    connection = sqlite3.connect("company.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM student")
    result = cursor.fetchall()
    for r in result:
        print(r)
        # def __init__(self, firstName, lastName, grade, address, discord_id, contact_number):
        student_list.append(Student(
            db_id=r[0],
            firstName=r[1],
            lastName=r[2],
            address=r[3],
            grade=r[4],
            discord_id=r[5],
            topic_list=add_topics_from_str(r[6]),
            contact_number=r[7]
        ))

    connection.commit()
    connection.close()


def add_topics_from_str(topic_str):
    # When loading from the database, topics are retrieved as strings
    # Take the string and return a list of class fellas
    # Revise code?
    topic_list = []
    module_name = 'generate_sheet'
    module_info = pyclbr.readmodule(module_name)
    for item in module_info.values():
        if item.name in topic_str and 'default_num' in item.methods:
            topic_list.append(item)

    return topic_list