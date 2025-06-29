from obj_q_gen.question_extraction import QuestionExtractor
from obj_q_gen.incorrect_answer_generation import IncorrectAnswerGenerator
import re
from nltk import sent_tokenize

class QuestionGeneration:
    '''This class contains the method
    to generate questions
    '''
    def __init__(self, num_questions, num_options):
        self.num_questions = num_questions
        self.num_options = num_options
        self.question_extractor = QuestionExtractor(num_questions)

    def generate_questions_dict(self, document):
        document = self.clean_text(document)

        self.questions_dict = self.question_extractor.get_questions_dict(document)

        incorrect_answer_generator = IncorrectAnswerGenerator(document)

        for i in range(1, self.num_questions + 1):
            if i not in self.questions_dict:
                continue
            self.questions_dict[i]["options"] = incorrect_answer_generator.get_all_options_dict(
                self.questions_dict[i]["answer"],
                self.num_options
            )

        return self.questions_dict

    def clean_text(self, text):
        text = text.lower()  # convert to lowercase
        text = text.replace('\n', ' ')  # remove newline chars
        sentences = sent_tokenize(text)
        cleaned_text = ""
        for sentence in sentences:
            # remove non-alphanumeric chars
            cleaned_sentence = re.sub(r'([^\s\w]|_)+', '', sentence)

            # substitute multiple spaces with a single space
            cleaned_sentence = re.sub(' +', ' ', cleaned_sentence)
            cleaned_text += cleaned_sentence

            if cleaned_text[-1] == ' ':
                cleaned_text = cleaned_text[:-1] + '.'
            else:
                cleaned_text += '.'

            cleaned_text += ' '  # pad with space at the end
        return cleaned_text
