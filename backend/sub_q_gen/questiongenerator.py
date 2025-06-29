import en_core_web_sm
import json
import numpy as np
import random
import re
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    AutoModelForSequenceClassification,
    T5Tokenizer,
    T5ForConditionalGeneration,
)
from typing import Any, List, Mapping, Tuple
import warnings

warnings.filterwarnings("ignore", message=".*Converting from Tiktoken failed.*")


class QuestionGenerator:
    def __init__(self) -> None:
        QG_PRETRAINED = "iarfmoose/t5-base-question-generator"
        self.ANSWER_TOKEN = "<answer>"
        self.CONTEXT_TOKEN = "<context>"
        self.SEQ_LENGTH = 512
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.qg_tokenizer = T5Tokenizer.from_pretrained(QG_PRETRAINED, legacy=False, use_fast=False)
        self.qg_model = T5ForConditionalGeneration.from_pretrained(QG_PRETRAINED)
        self.qg_model.to(self.device)
        self.qg_model.eval()
        self.qa_evaluator = QAEvaluator()

    def generate(self, article: str, use_evaluator: bool = True, num_questions: int = None, answer_style: str = "all") -> List:
        print("Generating questions...\n")
        qg_inputs, qg_answers = self.generate_qg_inputs(article, answer_style)
        generated_questions = self.generate_questions_from_inputs(qg_inputs)
        
        assert len(generated_questions) == len(qg_answers), f"{len(generated_questions)} questions doesn't match {len(qg_answers)} answers"

        if use_evaluator and self.qa_evaluator.evaluator_available:
            print("Evaluating QA pairs...\n")
            encoded_qa_pairs = self.qa_evaluator.encode_qa_pairs(generated_questions, qg_answers)
            scores = self.qa_evaluator.get_scores(encoded_qa_pairs)
            qa_list = self._get_ranked_qa_pairs(generated_questions, qg_answers, scores, num_questions or 10)
        else:
            print("Skipping evaluation step.\n")
            qa_list = self._get_all_qa_pairs(generated_questions, qg_answers)
            if num_questions and len(qa_list) > num_questions:
                qa_list = qa_list[:num_questions]

        return qa_list

    def generate_qg_inputs(self, text: str, answer_style: str) -> Tuple[List[str], List[str]]:
        VALID_ANSWER_STYLES = ["all", "sentences", "multiple_choice"]
        if answer_style not in VALID_ANSWER_STYLES:
            raise ValueError(f"Invalid answer style {answer_style}. Please choose from {VALID_ANSWER_STYLES}")

        inputs = []
        answers = []

        if answer_style in ["sentences", "all"]:
            segments = self._split_into_segments(text)
            for segment in segments:
                sentences = self._split_text(segment)
                prepped_inputs, prepped_answers = self._prepare_qg_inputs(sentences, segment)
                inputs.extend(prepped_inputs)
                answers.extend(prepped_answers)

        if answer_style in ["multiple_choice", "all"]:
            sentences = self._split_text(text)
            prepped_inputs, prepped_answers = self._prepare_qg_inputs_MC(sentences)
            inputs.extend(prepped_inputs)
            answers.extend(prepped_answers)

        return inputs, answers

    def generate_questions_from_inputs(self, qg_inputs: List) -> List[str]:
        generated_questions = []
        for qg_input in qg_inputs:
            question = self._generate_question(qg_input)
            generated_questions.append(question)
        return generated_questions

    def _split_text(self, text: str) -> List[str]:
        MAX_SENTENCE_LEN = 128
        sentences = re.findall(".*?[.!\?]", text)
        cut_sentences = []

        for sentence in sentences:
            if len(sentence) > MAX_SENTENCE_LEN:
                cut_sentences.extend(re.split("[,;:)]", sentence))

        cut_sentences = [s for s in sentences if len(s.split(" ")) > 5]
        sentences = sentences + cut_sentences
        return list(set([s.strip(" ") for s in sentences]))

    def _split_into_segments(self, text: str) -> List[str]:
        MAX_TOKENS = 490
        paragraphs = text.split("\n")
        tokenized_paragraphs = []
        
        for p in paragraphs:
            if len(p) > 0:
                tokens = self.qg_tokenizer(p, return_tensors="pt", truncation=True, max_length=512)["input_ids"][0].tolist()
                tokenized_paragraphs.append(tokens)
        
        segments = []
        while len(tokenized_paragraphs) > 0:
            segment = []
            while len(segment) < MAX_TOKENS and len(tokenized_paragraphs) > 0:
                paragraph = tokenized_paragraphs.pop(0)
                segment.extend(paragraph)
            segments.append(segment)

        return [self.qg_tokenizer.decode(s, skip_special_tokens=True) for s in segments]

    def _prepare_qg_inputs(self, sentences: List[str], text: str) -> Tuple[List[str], List[str]]:
        inputs = []
        answers = []
        for sentence in sentences:
            qg_input = f"{self.ANSWER_TOKEN} {sentence} {self.CONTEXT_TOKEN} {text}"
            inputs.append(qg_input)
            answers.append(sentence)
        return inputs, answers

    def _prepare_qg_inputs_MC(self, sentences: List[str]) -> Tuple[List[str], List[str]]:
        spacy_nlp = en_core_web_sm.load()
        docs = list(spacy_nlp.pipe(sentences, disable=["parser"]))
        inputs_from_text = []
        answers_from_text = []

        for doc, sentence in zip(docs, sentences):
            entities = doc.ents
            if entities:
                for entity in entities:
                    qg_input = f"{self.ANSWER_TOKEN} {entity} {self.CONTEXT_TOKEN} {sentence}"
                    answers = self._get_MC_answers(entity, docs)
                    inputs_from_text.append(qg_input)
                    answers_from_text.append(answers)

        return inputs_from_text, answers_from_text

    def _get_MC_answers(self, correct_answer: Any, docs: Any) -> List[Mapping[str, Any]]:
        entities = []
        for doc in docs:
            entities.extend([{"text": e.text, "label_": e.label_} for e in doc.ents])

        entities_json = [json.dumps(kv) for kv in entities]
        pool = set(entities_json)
        num_choices = min(4, len(pool)) - 1

        final_choices = []
        correct_label = correct_answer.label_
        final_choices.append({"answer": correct_answer.text, "correct": True})
        
        pool.discard(json.dumps({"text": correct_answer.text, "label_": correct_answer.label_}))

        matches = [e for e in pool if correct_label in e]

        if len(matches) < num_choices:
            choices = matches
            pool = pool.difference(set(choices))
            if len(pool) > 0:
                choices.extend(random.sample(list(pool), min(num_choices - len(choices), len(pool))))
        else:
            choices = random.sample(matches, num_choices)

        choices = [json.loads(s) for s in choices]
        for choice in choices:
            final_choices.append({"answer": choice["text"], "correct": False})

        random.shuffle(final_choices)
        return final_choices

    @torch.no_grad()
    def _generate_question(self, qg_input: str) -> str:
        encoded_input = self._encode_qg_input(qg_input)
        output = self.qg_model.generate(
            input_ids=encoded_input["input_ids"],
            max_length=64,
            num_beams=4,
            early_stopping=True,
            do_sample=False
        )
        question = self.qg_tokenizer.decode(output[0], skip_special_tokens=True)
        return question

    def _encode_qg_input(self, qg_input: str) -> dict:
        encoding = self.qg_tokenizer(
            qg_input,
            padding='max_length',
            max_length=self.SEQ_LENGTH,
            truncation=True,
            return_tensors="pt",
        )
        return {k: v.to(self.device) for k, v in encoding.items()}

    def _get_ranked_qa_pairs(self, generated_questions: List[str], qg_answers: List[str], scores, num_questions: int = 10) -> List[Mapping[str, str]]:
        if num_questions > len(scores):
            num_questions = len(scores)
            print(f"\nWas only able to generate {num_questions} questions. For more questions, please input a longer text.")

        qa_list = []
        for i in range(num_questions):
            index = scores[i]
            qa = {
                "question": generated_questions[index].split("?")[0] + "?",
                "answer": qg_answers[index]
            }
            qa_list.append(qa)
        return qa_list

    def _get_all_qa_pairs(self, generated_questions: List[str], qg_answers: List[str]):
        qa_list = []
        for question, answer in zip(generated_questions, qg_answers):
            qa = {
                "question": question.split("?")[0] + "?",
                "answer": answer
            }
            qa_list.append(qa)
        return qa_list


class QAEvaluator:
    def __init__(self) -> None:
        QAE_PRETRAINED = "iarfmoose/bert-base-cased-qa-evaluator"
        self.SEQ_LENGTH = 512
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.qae_tokenizer = AutoTokenizer.from_pretrained(QAE_PRETRAINED, use_fast=False)
        self.qae_model = AutoModelForSequenceClassification.from_pretrained(QAE_PRETRAINED)
        self.qae_model.to(self.device)
        self.qae_model.eval()
        self.evaluator_available = True

    def encode_qa_pairs(self, questions: List[str], answers: List[str]) -> List[torch.tensor]:
        encoded_pairs = []
        for question, answer in zip(questions, answers):
            encoded_qa = self._encode_qa(question, answer)
            encoded_pairs.append(encoded_qa)
        return encoded_pairs

    def get_scores(self, encoded_qa_pairs: List[torch.tensor]) -> List[int]:
        scores = {}
        for i in range(len(encoded_qa_pairs)):
            scores[i] = self._evaluate_qa(encoded_qa_pairs[i])
        return [k for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)]

    def _encode_qa(self, question: str, answer: str) -> dict:
        if type(answer) is list:
            correct_answer = next((a["answer"] for a in answer if a["correct"]), answer[0]["answer"])
        else:
            correct_answer = answer

        encoding = self.qae_tokenizer(
            text=question,
            text_pair=correct_answer,
            padding="max_length",
            max_length=self.SEQ_LENGTH,
            truncation=True,
            return_tensors="pt",
        )
        return {k: v.to(self.device) for k, v in encoding.items()}

    @torch.no_grad()
    def _evaluate_qa(self, encoded_qa_pair: dict) -> float:
        output = self.qae_model(**encoded_qa_pair)
        return float(output.logits[0][1])


def print_qa(qa_list: List[Mapping[str, str]], show_answers: bool = True) -> None:
    for i in range(len(qa_list)):
        space = " " * (3 if i < 9 else 4)
        print(f"{i + 1}) Q: {qa_list[i]['question']}")
        answer = qa_list[i]["answer"]

        if type(answer) is list:
            if show_answers:
                print(f"{space}A: 1. {answer[0]['answer']} {'(correct)' if answer[0]['correct'] else ''}")
                for j in range(1, len(answer)):
                    correct_marker = '(correct)' if answer[j]['correct'] else ''
                    print(f"{space + '   '}{j + 1}. {answer[j]['answer']} {correct_marker}")
            else:
                print(f"{space}A: 1. {answer[0]['answer']}")
                for j in range(1, len(answer)):
                    print(f"{space + '   '}{j + 1}. {answer[j]['answer']}")
            print("")
        else:
            if show_answers:
                print(f"{space}A: {answer}\n")