# Initialize the app and database:
# This makes sure the database system understands the flask app.
# It also adds a set of data to test with.
from app import app, db
from models.question__and_choice_model import Question, Choice
from models.surveyModel import Survey
from models.SurveyQuestionModel import SurveyQuestion
from models.userModel import User


def create_test_db():
    print("checking whether to create test DB")
    with app.app_context():

        db.create_all()

        # add test user
        if User.query.filter_by(email="tim.seip@capgemini.com").first() is not None:
            print("test user exists, not creating test dataset")
        else:
            print("inserting test dataset")
            user = User(email="tim.seip@capgemini.com", name="admin")
            user.set_password("adminpw")
            db.session.add(user)

            # add test survey
            survey = Survey(survey_name="Quick Scan test version")

            db.session.add(survey)

            # add test questions
            TQ1 = Question(question_type=0, question_text="Is de winkel goed bereikbaar met het openbaar vervoer?")  # yes/no
            TQ2 = Question(question_type=1, question_text="Is er voldoende parkeergelegenheid bij de winkel?")  # multiple choice one answer
            TQ3 = Question(question_type=0, question_text="Zijn er alternatieve verkooppunten in de omgeving met vergelijkbare producten of diensten?")  # yes/no
            TQ4 = Question(question_type=1, question_text="Wordt de klant begroet bij binnenkomst?")  # multiple choice one answer
            TQ5 = Question(question_type=3, question_text="Welke manier van prijscommunicatie (schapkaartjes, stickers, etc.) worden er gebruikt?")  # open
            TQ6 = Question(question_type=3, question_text="Hoe wordt er afgeprijsd? (Handmatig? Of met ESLs?).")  # open
            TQ7 = Question(question_type=0, question_text="Is er additionele productinformatie beschikbaar?")  # yes/no
            TQ8 = Question(question_type=0, question_text="Zijn er IT oplossingen ingezet om klanten te ondersteunen in hun koopproces?")  # yes/no
            TQ9 = Question(question_type=3, question_text="Wat is het THT beleid?")  # open
            TQ10 = Question(question_type=1, question_text="Worden er schapwissels regelmatig doorgevoerd?")  # multiple choice one answer
            TQ11 = Question(question_type=1, question_text="Hoe vaak wordt het filiaal beleverd, en hoe vaak wordt de levering aangevuld?")  # multiple choice one answer
            TQ12 = Question(question_type=1, question_text="Hoe wordt het personeel ingeroosterd? Wordt er een WFM tool gebruikt, of gebeurt dit handmatig?")  # multiple choice one answer
            TQ13 = Question(question_type=3, question_text="Wat is het ziekteverzuimpercentage?")  # open
            TQ14 = Question(question_type=2, question_text="Welke betaalmogelijkheden zijn er?")  # multiple choice multiple answer
            TQ15 = Question(question_type=0, question_text="Is het mogelijk om producten in de winkel te retourneren?")  # yes/no
            TQ16 = Question(question_type=0, question_text="Is er een webshop beschikbaar?")  # yes/no
            TQ17 = Question(question_type=0, question_text="Kunnen online gekochte producten in de winkel gerouterneerd worden?")  # yes/no

            db.session.add(TQ1)
            db.session.add(TQ2)
            db.session.add(TQ3)
            db.session.add(TQ4)
            db.session.add(TQ5)
            db.session.add(TQ6)
            db.session.add(TQ7)
            db.session.add(TQ8)
            db.session.add(TQ9)
            db.session.add(TQ10)
            db.session.add(TQ11)
            db.session.add(TQ12)
            db.session.add(TQ13)
            db.session.add(TQ14)
            db.session.add(TQ15)
            db.session.add(TQ16)
            db.session.add(TQ17)

            # link test questions to test survey
            SQ1 = SurveyQuestion(question_id=1, survey_id=1, category_weight_one=4,
            category_weight_two=1, category_weight_three=1, category_weight_four=1, category_weight_five=1)

            SQ2 = SurveyQuestion(question_id=2, survey_id=1, category_weight_one=4,
            category_weight_two=1, category_weight_three=1, category_weight_four=1, category_weight_five=1)

            SQ3 = SurveyQuestion(question_id=3, survey_id=1, category_weight_one=1,
            category_weight_two=1, category_weight_three=1, category_weight_four=4, category_weight_five=1)

            SQ4 = SurveyQuestion(question_id=4, survey_id=1, category_weight_one=1,
            category_weight_two=1, category_weight_three=4, category_weight_four=1, category_weight_five=2)

            SQ5 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
            category_weight_two=4, category_weight_three=2, category_weight_four=1, category_weight_five=1)

            SQ6 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
            category_weight_two=4, category_weight_three=1, category_weight_four=1, category_weight_five=1)

            SQ7 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
            category_weight_two=1, category_weight_three=2, category_weight_four=4, category_weight_five=1)

            SQ8 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
            category_weight_two=1, category_weight_three=4, category_weight_four=1, category_weight_five=4)

            SQ9 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
            category_weight_two=1, category_weight_three=1, category_weight_four=4, category_weight_five=1)

            SQ10 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
            category_weight_two=1, category_weight_three=3, category_weight_four=4, category_weight_five=3)

            SQ11 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
            category_weight_two=1, category_weight_three=3, category_weight_four=4, category_weight_five=3)

            SQ12 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
            category_weight_two=1, category_weight_three=4, category_weight_four=1, category_weight_five=3)

            SQ13 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
            category_weight_two=1, category_weight_three=2, category_weight_four=1, category_weight_five=1)

            SQ14 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
            category_weight_two=4, category_weight_three=3, category_weight_four=1, category_weight_five=4)

            SQ15 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=1,
            category_weight_two=1, category_weight_three=2, category_weight_four=1, category_weight_five=4)

            SQ16 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=4,
            category_weight_two=1, category_weight_three=3, category_weight_four=1, category_weight_five=3)

            SQ17 = SurveyQuestion(question_id=5, survey_id=1, category_weight_one=2,
            category_weight_two=1, category_weight_three=2, category_weight_four=1, category_weight_five=4)

            db.session.add(SQ1)
            db.session.add(SQ2)
            db.session.add(SQ3)
            db.session.add(SQ4)
            db.session.add(SQ5)
            db.session.add(SQ6)
            db.session.add(SQ7)
            db.session.add(SQ8)
            db.session.add(SQ9)
            db.session.add(SQ10)
            db.session.add(SQ11)
            db.session.add(SQ12)
            db.session.add(SQ13)
            db.session.add(SQ14)
            db.session.add(SQ15)
            db.session.add(SQ16)
            db.session.add(SQ17)

            # give the multiple choice questions possible choices
            # give the multiple choice questions possible choices
            C1 = Choice(question=TQ2, choice_text="Voldoet niet.")
            C2 = Choice(question=TQ2, choice_text="Voldoet deels.")
            C3 = Choice(question=TQ2, choice_text="Voldoet.")
            C4 = Choice(question=TQ2, choice_text="Ruim voldoende.")
            C5 = Choice(question=TQ4, choice_text="Ja, door al het personeel.")
            C6 = Choice(question=TQ4, choice_text="Ja, door een deel van het personeel.")
            C7 = Choice(question=TQ4, choice_text="Nee.")
            C8 = Choice(question=TQ10, choice_text="Dagelijks.")
            C9 = Choice(question=TQ10, choice_text="Wekelijks.")
            C10 = Choice(question=TQ10, choice_text="Maandelijks.")
            C11 = Choice(question=TQ10, choice_text="Elk kwartaal.")
            C12 = Choice(question=TQ10, choice_text="Elk halfjaar.")
            C13 = Choice(question=TQ10, choice_text="Jaarlijks.")
            C14 = Choice(question=TQ12, choice_text="Volledig geautomatiseerd.")
            C15 = Choice(question=TQ12, choice_text="Deels geautomatiseerd.")
            C16 = Choice(question=TQ12, choice_text="Volledig handmatig.")
            C17 = Choice(question=TQ14, choice_text="Contant.")
            C18 = Choice(question=TQ14, choice_text="Pinpas.")
            C19 = Choice(question=TQ14, choice_text="Creditcard..")
            C20 = Choice(question=TQ14, choice_text="Cadeaubon.")
            C21 = Choice(question=TQ14, choice_text="VVV bon.")
            C22 = Choice(question=TQ14, choice_text="Anders (gebruik tekstveld).")

            db.session.add(C1)
            db.session.add(C2)
            db.session.add(C3)
            db.session.add(C4)
            db.session.add(C5)
            db.session.add(C6)
            db.session.add(C7)
            db.session.add(C8)
            db.session.add(C9)
            db.session.add(C10)
            db.session.add(C11)
            db.session.add(C12)
            db.session.add(C13)
            db.session.add(C14)
            db.session.add(C15)
            db.session.add(C16)
            db.session.add(C17)
            db.session.add(C18)
            db.session.add(C19)
            db.session.add(C20)
            db.session.add(C21)

            # commit all this to the DB
            db.session.commit()
            print("test dataset added")
