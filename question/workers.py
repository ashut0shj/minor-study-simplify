from question_generation_main import QuestionGeneration
def cont(dic):
    l = []
    for i in dic:
        element = dic[i]
        que = element['question'] + ',' + element['answer']
        for j in element['options']  :
            que = que + ',' + j
        l.append(que)    
    return l

def get_user_input() -> str:
    """ Get text input from the user """
    return input("Enter the text: ")

def text2questions(text_content: str, n=5, o=4) -> dict:
    """ Get all questions and options from text content """
    qGen = QuestionGeneration(n, o)
    q = qGen.generate_questions_dict(text_content)
    
    for i in range(len(q)):
        temp = []
        for j in range(len(q[i + 1]['options'])):
            temp.append(q[i + 1]['options'][j + 1])
        q[i + 1]['options'] = temp

    return q

# Get user input
text_content = get_user_input()

# Generate questions and options from the user input text
questions_dict = text2questions(text_content)

file = open('quest.txt','w+')
for i in cont(questions_dict):
    print(i)
    file.write(i + '\n')
file.close()

#Print each question and options on separate lines
for question_number, question_data in questions_dict.items():
    print(f"Question {question_number}: {question_data['question']}")
    for option_number, option in enumerate(question_data['options'], start=1):
        print(f"  Option {option_number}: {option}")
    print(f"Answer: {question_data['answer']}\n")
