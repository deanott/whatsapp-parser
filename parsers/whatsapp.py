from datetime import datetime
import message

''' A line can be either: 
        09/12/2012 17:03:48: Sender Name: Message
        3/24/14, 1:59:59 PM: Sender Name: Message
        24/3/14, 13:59:59: Sender Name: Message
'''

class ParserWhatsapp():

    def __init__(self, raw_messages):
        self.raw_messages = raw_messages

    def parse(self):
        list_of_messages = []
        set_of_senders = set()
        for l in self.raw_messages:
            #BUG: Yeah well this isnt working...
            #Okay my test data is "03/10/2016, 9:27 pm - Cat: I like cats"
            #Whatsapp why you gotta update everything?
            msg_date, sep, msg = l.partition("- ")
            raw_date, sep, time = msg_date.partition(" ")
            sender, sep, content = msg.partition(": ")

            # This ignores a minority of bad formatted lines. A bad formatted line? What makes a date line bad? why would it format wrong?
            #BUG: Okay new problem, apparently whatsapp thinks it a great idea to when you get emailed the data for file attachments world and seperate out the next message
            #Real fix = dont download email with attachments!
            #BUG: Write for long enough whatasapp then creates a new line also. Fantastic.

            #Ignore minority of bad formatted lines. Caused by long paragraph and image attachments.
            #Checks length is within a limit of date
            #BUG: fudamentally flawed as if the conditions of extraction of the overline message matches this it won't work.
            # if len(raw_date) != 10 or len(time) != 8:
            #     continue

            # New whatsapp data test:
            if len(raw_date) != 11 or len(time) != 8:
                continue

            raw_date = raw_date.replace(",", "")
            year = raw_date.split(" ")[0].split("/")[-1]
            # The following lines treats:
            # 3/24/14 1:59:59 PM
            # 24/3/14 13:59:59 PM
            # Couldn't we use msg_date instead of chatTimeString here?

            # colonIndex = [x.start() for x in re.finditer(':', l)]
            # print l, colonIndex
            # chatTimeString = l[0:colonIndex[2]]
            if "AM" in msg_date or "PM" in msg_date:
                datetime_obj = datetime.strptime(
                    msg_date, "%m/%d/%y, %I:%M:%S %p")

            elif "am " in msg_date or "pm " in msg_date:
                datetime_obj = datetime.strptime(
                    msg_date, "%d/%m/%Y, %I:%M %p ")
                #To fit with analyse later format like the others
                sDateTime = datetime_obj.strftime("%m/%d/%y %H:%M:%S")
                datetime_obj = datetime.strptime(sDateTime, "%m/%d/%y %H:%M:%S")

            else:
                if len(year) == 2:
                    datetime_obj = datetime.strptime(msg_date, "%m/%d/%y %H:%M:%S")
                else:
                    datetime_obj = datetime.strptime(msg_date, "%m/%d/%Y %H:%M:%S")

            set_of_senders.add(sender)
            list_of_messages.append(message.Message(sender, content, raw_date, time, datetime_obj))

        return list(set_of_senders), list_of_messages
