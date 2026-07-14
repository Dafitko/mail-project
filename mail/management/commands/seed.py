import random
from django.core.management.base import BaseCommand
from mail.models import User, Email

class Command(BaseCommand):
    help = 'Seeds the database with 80+ funny Harry Potter dummy data emails'

    def handle(self, *args, **options):
        self.stdout.write("Deleting all existing emails and users...")
        Email.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("Creating Harry Potter universe users (password for all: test)...")
        users_info = {
            "harry@hogwarts.edu": "Harry Potter",
            "ron@hogwarts.edu": "Ron Weasley",
            "hermione@hogwarts.edu": "Hermione Granger",
            "dumbledore@hogwarts.edu": "Albus Dumbledore",
            "voldemort@deathlyhallows.com": "Lord Voldemort",
            "snape@hogwarts.edu": "Severus Snape",
        }

        users = {}
        for email, name in users_info.items():
            user = User.objects.create_user(username=email, email=email, password="test")
            user.save()
            users[email] = user
            self.stdout.write(f"  Created user: {name} ({email})")

        def create_email(sender_email, recipient_emails, subject, body, read_for_recipients=False, archived_for_recipients=False):
            sender = users[sender_email]
            recipients = [users[r] for r in recipient_emails]
            
            # Sender's copy
            email_sender = Email(
                user=sender,
                sender=sender,
                subject=subject,
                body=body,
                read=True,
                archived=False
            )
            email_sender.save()
            for r in recipients:
                email_sender.recipients.add(r)
            email_sender.save()
            
            # Recipients' copies
            for r in recipients:
                email_rec = Email(
                    user=r,
                    sender=sender,
                    subject=subject,
                    body=body,
                    read=read_for_recipients,
                    archived=archived_for_recipients
                )
                email_rec.save()
                for rec in recipients:
                    email_rec.recipients.add(rec)
                email_rec.save()

        self.stdout.write("Populating hand-crafted magical emails...")

        # 1. Ron -> Harry
        create_email(
            "ron@hogwarts.edu", ["harry@hogwarts.edu"],
            "Spells and Spiders",
            "Harry, Hermione is lecturing me again about my wand being taped together. Also, there is a giant spider in my left boot. Can I sleep in your dorm tonight? Please say yes.",
            read_for_recipients=False
        )

        # 2. Hermione -> Ron & Harry
        create_email(
            "hermione@hogwarts.edu", ["ron@hogwarts.edu", "harry@hogwarts.edu"],
            "IT IS LEVI-O-SA",
            "Ronald, I noticed you were pronouncing the Levitation Charm incorrectly again today. It is Levi-O-sa, not Levi-o-SAR. Also, both of you please do your Transfiguration homework before midnight. I will not let you copy mine this time!",
            read_for_recipients=True
        )

        # 3. Dumbledore -> Harry
        create_email(
            "dumbledore@hogwarts.edu", ["harry@hogwarts.edu"],
            "Sherbet Lemons and Danger",
            "Harry, please come to my office tonight. Bring the Invisibility Cloak. And no, this is not about your grades, though you really should pay more attention in Potions. The password is 'Acid Pops'.",
            read_for_recipients=False
        )

        # 4. Snape -> Harry
        create_email(
            "snape@hogwarts.edu", ["harry@hogwarts.edu"],
            "Detention",
            "Potter. Your lack of talent in Potions has reached a new low. You will report to my dungeon at 8 PM tonight to clean cauldron bottoms without magic. Do not be late, or I will deduct 50 points from Gryffindor.",
            read_for_recipients=True
        )

        # 5. Voldemort -> Harry
        create_email(
            "voldemort@deathlyhallows.com", ["harry@hogwarts.edu"],
            "Let's reschedule the battle",
            "Harry, my boy. June is extremely busy for my Death Eaters (Lucius has a gala, and Bellatrix is getting her hair done). Can we push our final battle to July? Also, I lost one of my horcruxes, a gold diadem. If you find it, please return it. Unopened. Thanks.",
            read_for_recipients=False
        )

        # 6. Harry -> Voldemort
        create_email(
            "harry@hogwarts.edu", ["voldemort@deathlyhallows.com"],
            "Re: Let's reschedule the battle",
            "No, Tom. July doesn't work for me, I have Quidditch camp. And I'm not returning your diadem. Hermione and Ron already destroyed it with a basilisk fang. Best of luck with the nose.",
            read_for_recipients=True,
            archived_for_recipients=True
        )

        # 7. Hermione -> Harry
        create_email(
            "hermione@hogwarts.edu", ["harry@hogwarts.edu"],
            "Library Hours Disaster",
            "Harry, the library is now closing at 9 PM instead of 10 PM. This is an absolute disaster! How am I supposed to finish my light reading on Ancient Runes (it is only 800 pages)? We need to write a petition to Dumbledore immediately.",
            read_for_recipients=True
        )

        # 8. Ron -> Hermione
        create_email(
            "ron@hogwarts.edu", ["hermione@hogwarts.edu"],
            "Re: Library Hours Disaster",
            "Hermione, please go to sleep.",
            read_for_recipients=True
        )

        # 9. Dumbledore -> Snape
        create_email(
            "dumbledore@hogwarts.edu", ["snape@hogwarts.edu"],
            "Shampoo recommendation",
            "Severus, I noticed your hair is looking a bit... sleek lately. I highly recommend the 'Sleekeazy's Hair Potion'. Or perhaps just water and soap? Let's discuss this over lemon drops and tea.",
            read_for_recipients=True
        )

        # 10. Snape -> Dumbledore
        create_email(
            "snape@hogwarts.edu", ["dumbledore@hogwarts.edu"],
            "Re: Shampoo recommendation",
            "Headmaster, I assure you my hygiene is of no concern to the school governors. I request that you focus on Potter's complete disregard for school rules instead of my hair.",
            read_for_recipients=True
        )

        # 11. Harry -> Ron
        create_email(
            "harry@hogwarts.edu", ["ron@hogwarts.edu"],
            "Quidditch Practice in a Storm",
            "Ron, practice is at 6 AM tomorrow. Wood is planning to fly through a thunderstorm to 'build character'. Bring a dry cloak and maybe some of Fred and George's Fever Fudge.",
            read_for_recipients=False
        )

        # 12. Voldemort -> Snape
        create_email(
            "voldemort@deathlyhallows.com", ["snape@hogwarts.edu"],
            "Performance Review",
            "Severus, why is the Potter boy still alive? You've been teaching him for five years. I'm starting to think you're not actually trying to poison his pumpkin juice. Please reply ASAP.",
            read_for_recipients=False
        )

        # 13. Snape -> Voldemort
        create_email(
            "snape@hogwarts.edu", ["voldemort@deathlyhallows.com"],
            "Re: Performance Review",
            "My Lord, the boy is constantly protected by Dumbledore's meddling and sheer dumb luck. I am slowly gaining his trust. Trust the process.",
            read_for_recipients=True,
            archived_for_recipients=True
        )

        # 14. Hermione -> Harry & Ron
        create_email(
            "hermione@hogwarts.edu", ["harry@hogwarts.edu", "ron@hogwarts.edu"],
            "S.P.E.W. Meeting",
            "Hello, just a reminder that the Society for the Promotion of Elfish Welfare (S.P.E.W.) meets today at 5 PM in the common room. Attendance is mandatory. I have made badges. They are neon green.",
            read_for_recipients=False
        )

        self.stdout.write("Generating 65 additional randomized magical emails...")
        
        topics = [
            {
                "subject": "Missing Cauldron",
                "body": "Has anyone seen my pewter cauldron? I left it near the Herbology greenhouse. If Neville took it again, I'm going to turn his shoes into teacups.",
            },
            {
                "subject": "Bertie Bott's Beans Warning",
                "body": "Do NOT eat the yellow ones from the new batch in Hogsmeade. I thought it was banana, but it was earwax combined with troll booger. You have been warned.",
            },
            {
                "subject": "Quidditch Match rescheduled",
                "body": "The match against Ravenclaw is moved to Friday morning due to heavy rain. Wood says we must practice flying blindfolded to prepare for the fog.",
            },
            {
                "subject": "Chocolate Frog trading",
                "body": "I have three Albus Dumbledore cards and two Merlin cards. I am willing to trade them for a single Gilderoy Lockhart card to complete my collection.",
            },
            {
                "subject": "Gringotts Account Update",
                "body": "Your vault has been assessed. Your balance remains at 3 galleons and 14 sickles. Please note that keeping baby dragons in your vault is strictly prohibited by Gringotts policy.",
            },
            {
                "subject": "Howler Warning",
                "body": "My mother is threatening to send a Howler because of my recent grade in Divination. If you hear screaming in the Great Hall tomorrow morning, please pretend you don't know me.",
            },
            {
                "subject": "Forbidden Forest warning",
                "body": "This is a reminder that the Forbidden Forest is off-limits to all students who do not wish to suffer a highly painful death. And yes, Hagrid, this includes your pets.",
            },
            {
                "subject": "Found: Invisibility Cloak?",
                "body": "I found a piece of empty air in the common room near the fireplace. It feels like silk but I can't see it at all. Please claim it if you lost your invisibility.",
            },
            {
                "subject": "Time-Turner scheduling conflict",
                "body": "I accidentally attended two classes at the same time and met myself in the hallway. We agreed to disagree on the transfiguration homework. It was quite bizarre.",
            },
            {
                "subject": "Marauder's Map password",
                "body": "I solemnly swear that I am up to no good. Please remember to manage your mischief once you are done reading your messages.",
            },
            {
                "subject": "Snape's stare",
                "body": "He looked at me for 10 seconds today without blinking during the lecture. I think he was trying to read my mind, or he was just really upset about my potion exploding.",
            },
            {
                "subject": "Daily Prophet subscription renewal",
                "body": "Your subscription is about to expire. Send 5 sickles via owl to renew. This week's headline: Dumbledore's new hat - fashion statement or dark magical artifact?",
            },
            {
                "subject": "Weasley Sweaters order",
                "body": "Mum is asking what color you want for this year's Christmas sweater. Choices are maroon, maroon, or slightly darker maroon. Please let me know ASAP.",
            },
            {
                "subject": "Floo Network maintenance",
                "body": "Please be advised that the Floo Network connections in the Gryffindor common room fireplace will be down for maintenance this Tuesday. Use the stairs.",
            },
            {
                "subject": "Mandragora handling rules",
                "body": "Earmuffs are mandatory. Neville forgot his earmuffs today and fainted immediately. Professor Sprout is not pleased. Please read the manual.",
            }
        ]

        users_list = list(users_info.keys())
        
        # Set a seed to make it reproducible
        random.seed(42)
        
        for i in range(1, 66):
            sender_email = random.choice(users_list)
            recipient_candidates = [u for u in users_list if u != sender_email]
            recipient_email = random.choice(recipient_candidates)
            
            topic = random.choice(topics)
            subject = f"{topic['subject']} (Msg #{i})"
            body = f"Dear {users_info[recipient_email]},\n\n{topic['body']}\n\nSincerely,\n{users_info[sender_email]}"
            
            # Assign random read/unread/archived states
            read_state = random.choice([True, False])
            archived_state = random.choice([True, False]) if read_state else False
            
            create_email(
                sender_email, [recipient_email],
                subject, body,
                read_for_recipients=read_state,
                archived_for_recipients=archived_state
            )

        total_emails = Email.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Database seeded successfully with {total_emails} magical email records!"))
