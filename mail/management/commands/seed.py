from django.core.management.base import BaseCommand
from mail.models import User, Email

class Command(BaseCommand):
    help = 'Seeds the database with funny Harry Potter dummy data'

    def handle(self, *args, **options):
        self.stdout.write("Deleting all existing emails and users...")
        Email.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("Creating Harry Potter universe users (password for all: password123)...")
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
            user = User.objects.create_user(username=email, email=email, password="password123")
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

        self.stdout.write("Populating magical emails...")

        # 1. Ron -> Harry
        create_email(
            "ron@hogwarts.edu", ["harry@hogwarts.edu"],
            "Spells and Spiders",
            "Harry, Hermione is lecturing me again about my wand being taped together. Also, there is a giant spider in my left boot. Can I sleep in your dorm tonight? Please say yes.",
            read_for_recipients=False
        )

        # 2. Hermione -> Ron (and CC Harry, which in this model means sending to both)
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

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with Harry Potter universe data!"))
