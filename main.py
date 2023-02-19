calls_counter = {}  # global calls counter storage


def count_calls(cb):
    def wrapper(*a, **kw):
        try:
            calls_counter[cb.__name__] += 1
        except:
            calls_counter[cb.__name__] = 1
        return cb(*a, **kw)

    return wrapper


class Person:
    def __init__(self, name, age, experience, req_salary, looking_position):
        self.name = name
        self.age = age
        self.experience = experience  # experience in years
        self.req_salary = req_salary  # requested salary in dollars
        self.looking_position = (
            looking_position  # looking for this position in next company
        )

    @count_calls
    def say_hi(self):
        print(
            f"Hi! Im {self.name} {self.age} yo my experience {self.experience} years I request a salary of {self.req_salary} $. Im looking for {self.looking_position} position in next company"
        )


class Worker(Person):
    def __init__(
        self,
        name,
        age,
        experience,
        req_salary,
        looking_position,
        working_now,
        position,
        current_salary,
    ):
        super().__init__(name, age, experience, req_salary, looking_position)
        self.working_now = working_now.name  # company name
        self.position = position
        self.current_salary = current_salary

    @count_calls
    def say_hi(self):
        super().say_hi()
        print(
            f"Im work in {self.working_now} my position {self.position} and current salary {self.current_salary} $"
        )

    @count_calls
    def _get_message(self, from_company, message):
        print(
            f"[{self.name}] {self.name}, you got message from {from_company.name}: {message}"
        )


class Company:
    def __init__(
        self, name, description, max_staff, salary, work_group, ratio_over_salary
    ):
        self.name = name
        self.description = description
        self.max_staff = max_staff  # max count of staff
        self.salary = salary  # staring salary for [junior, middle, senior] in dollars
        self.work_group = work_group  # team workers in this company
        self.ratio_over_salary = (
            ratio_over_salary  # the coefficient of overpayment of salary
        )

    # contest among applicants
    @count_calls
    def contest(self, applicants, count_places):
        # if applicants require salary more than min of his position * 0.3 * max coefficient of overpayment of salary he will skipped

        people = sorted(
            applicants, key=lambda applicant: applicant.experience, reverse=True
        )

        while len(people) and count_places > 0:
            applicant_position_index = 0

            # get applicant position index
            for position_index in range(len(self.salary)):
                if people[0].looking_position == "junior":
                    applicant_position_index = position_index
                if people[0].looking_position == "middle":
                    applicant_position_index = position_index
                if people[0].looking_position == "senior":
                    applicant_position_index = position_index

            if (
                people[0].req_salary
                <= self.salary[applicant_position_index] * 0.3 * self.ratio_over_salary
            ):
                self.work_group.append(people[0])
                count_places -= 1

            del people[0]

    # print current work group
    @count_calls
    def current_group(self):
        print("Current workers group:", *[i.name for i in self.work_group])

    # print all information about company
    @count_calls
    def about_company(self):
        print("Company name:", self.name)
        print("Company description:", self.description)
        print("Company max count staff: ", self.max_staff)
        print(
            f"Company salary for \n\tjunior: {self.salary[0]} \n\tmiddle: { self.salary[1] }\n\tsenior: {self.salary[2]}"
        )

    # employ without contest in company
    @count_calls
    def employ(self, person):
        self.work_group.append(person)

    # fire person
    @count_calls
    def fire(self, person):
        group = self.work_group
        for i in range(len(group)):
            if group[i] == person:
                del group[i]
                break
        self.work_group = group

    # send email
    @count_calls
    def send_corporate_email(self, to_person, message):
        # to_person.get_message(self.name, message)
        try:
            to_person._get_message(self, message)
            print(f"[{self.name}] Message sended to {to_person.name}!")
        except:
            person_name = (
                to_person.name
                if type(to_person).__name__ == "Person"
                else "unknown person"
            )

            print(
                f"{[self.name]} Failed send message to {person_name}: this person doesn't work anywhere  "
            )


"""
class Person  - default person -> (name, age, experience, req_salary)
class Worker  - currently working person in some company -> (name, age, experience, req_salary, working_now, position, current_salary)
class Company - company -> (name, description, max_staff, salary, work_group)
"""

# * companies
VVS_company = Company(
    "VVS company", "Best solve for your business", 30, [1000, 3000, 4500], [], 1.45
)
Diamonds_crime_company = Company(
    "Diamonds crime", "Design UI", 12, [800, 2200, 3700], [], 1.25
)

# * people
dan = Person("Dan", 25, 0, 1200, "junior")
jacob = Person("Jacob", 20, 0, 700, "junior")
ben = Person("Ben", 24, 3, 950, "middle")
john = Person("John", 27, 5, 1200, "senior")
wilson = Person("Wilson", 39, 17, 6600, "senior")

# * workers
bruce = Worker("Bruce", 23, 3, 1800, "middle", Diamonds_crime_company, "junior", 1200)
jack = Worker("Jack", 29, 7, 3900, "senior", Diamonds_crime_company, "middle", 3700)
alex = Worker("Alex", 32, 10, 6400, "senior", Diamonds_crime_company, "senior", 6000)

# * testing

john.say_hi()
# jack.say_hi()
# wilson.say_hi()
# alex.say_hi()

VVS_company.about_company()
# Diamonds_crime_company.about_company()

# * Editing group

Diamonds_crime_company.employ(bruce)
Diamonds_crime_company.employ(jack)
Diamonds_crime_company.employ(alex)

Diamonds_crime_company.current_group()

# * Contest

VVS_company.current_group()
VVS_company.contest([dan, jacob, ben, john, wilson, bruce, jack, alex], 5)
VVS_company.current_group()

print("\n")

# * Sending messages

VVS_company.send_corporate_email(alex, "Hello, maybe fire Bruce ? ")
VVS_company.send_corporate_email(dan, "Hi! How's going on super secret project ?")
Diamonds_crime_company.send_corporate_email(VVS_company, "Are you human or what ?")
Diamonds_crime_company.send_corporate_email("Edward", "Are you human or what ?")

print("\n")

print(calls_counter)

# Only Alex can get corporate email from company, because he work in some company

# Alex is worker
# Dan is person
# VVS_company is company
# "Edward" is string
