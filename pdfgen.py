import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Matrix, Alignat
from pylatex.utils import italic, bold
import pdflatex
from models.ParticipationModel import participation_schema, Participation
from models.question__and_choice_model import question_schema, Question
from models.AnswerModel import Answer

def generate_document(participation_id):

    participation = Participation.query.get(participation_id)
    ref_key = participation.reference_key
    date = participation.created_date

    questions = Question.query.all()
    
    for question in questions:
        print(question.question_text)

    # participation = participation_schema.dump(participation)


    geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section('Quick Scan Survey: %s' % ref_key)):
        doc.append('This document contains the results of the survey conducted on: %s. ' % date)
        doc.append('You can find the questions and their results below. \
        Please be aware that this document generation system \
        is in early stages, it is possible for items to not fit pages properly \
            or other odd things to happen. \n')
        
        for question in questions:
            answers =  Answer.query.filter_by(participation_key = participation_id)
            doc.append('\n')
            doc.append("%s: %s " % (question.id, question.question_text))
            doc.append('\n')

            for answer in answers:
                if answer.question_key == question.id:
                    if question.question_type == 0:
                        print(answer.bool_answer)
                        doc.append('\n')
                        doc.append('   %s' % answer.bool_answer)
                    
            

        with doc.create(Subsection('Table of something')):
            with doc.create(Tabular('rc|cl')) as table:
                table.add_hline()
                table.add_row((1, 2, 3, 4))
                table.add_hline(1, 2)
                table.add_empty_row()
                table.add_row((4, 5, 6, 7))

    a = np.array([[100, 10, 20]]).T
    M = np.matrix([[2, 3, 4],
                    [0, 0, 1],
                    [0, 0, 2]])

    with doc.create(Section('The fancy stuff')):
        with doc.create(Subsection('Correct matrix equations')):
            doc.append(Math(data=[Matrix(M), Matrix(a), '=', Matrix(M * a)]))

        with doc.create(Subsection('Alignat math environment')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                agn.append(r'\frac{a}{b} &= 0 \\')
                agn.extend([Matrix(M), Matrix(a), '&=', Matrix(M * a)])

        with doc.create(Subsection('Beautiful graphs')):
            with doc.create(TikZ()):
                plot_options = 'height=4cm, width=6cm, grid=major'
                with doc.create(Axis(options=plot_options)) as plot:
                    plot.append(Plot(name='model', func='-x^5 - 242'))

                    coordinates = [
                        (-4.77778, 2027.60977),
                        (-3.55556, 347.84069),
                        (-2.33333, 22.58953),
                        (-1.11111, -493.50066),
                        (0.11111, 46.66082),
                        (1.33333, -205.56286),
                        (2.55556, -341.40638),
                        (3.77778, -1169.24780),
                        (5.00000, -3269.56775),
                    ]

                    plot.append(Plot(name='estimate', coordinates=coordinates))


    doc.generate_pdf('full', clean_tex=False)
