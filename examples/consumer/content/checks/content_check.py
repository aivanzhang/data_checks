import pandas as pd
from data_checks import DataCheck
import openai

openai.api_key = "SECRET KEY HERE"


class ContentCheck(DataCheck):
    content_data = pd.read_csv("examples/consumer/content/data.csv")

    def openai_checker(self, message: str, check_for: str):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'You will be provided with a message, and your task is to tell me if the message has {check_for}. Return "True" if it is, otherwise "False". The message is: "{message}".',
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].text.strip() == "True"

    @classmethod
    def defined_rules(cls) -> list[str]:
        return [
            "no_personal_data",
            "no_spam",
            "no_incoherent_content",
            "no_offensive_content",
            "no_misinformation",
            "no_hate_speech",
            "no_strong_language",
            "no_adult_content",
            "no_bot_content",
            "no_long_suspicous_urls",
            "no_extremely_negative_sentiment",
        ]

    def no_personal_data(self):
        for message in self.content_data["Content"]:
            response = self.openai_checker(message, "personal data")
            assert response == False, f"Message: `{message}` may contain personal data"

    def no_spam(self):
        for message in self.content_data["Content"]:
            response = self.openai_checker(message, "spam")
            assert response == False, f"Message: `{message}` may contain spam"

    def no_incoherent_content(self):
        for message in self.content_data["Content"]:
            response = self.openai_checker(message, "incoherent content")
            assert (
                response == False
            ), f"Message: `{message}` may contain incoherent content"

    def no_offensive_content(self):
        for message in self.content_data["Content"]:
            response = self.openai_checker(message, "offensive content")
            assert (
                response == False
            ), f"Message: `{message}` may contain offensive content"

    def no_misinformation(self):
        for message in self.content_data["Content"]:
            response = self.openai_checker(message, "misinformation")
            assert response == False, f"Message: `{message}` may contain misinformation"

    def no_hate_speech(self):
        for message in self.content_data["Content"]:
            response = self.openai_checker(message, "hate speech")
            assert response == False, f"Message: `{message}` may contain hate speech"

    def no_strong_language(self):
        for message in self.content_data["Content"]:
            response = self.openai_checker(message, "strong language")
            assert (
                response == False
            ), f"Message: `{message}` may contain strong language"

    def no_adult_content(self):
        for message in self.content_data["Content"]:
            response = self.openai_checker(message, "adult content")
            assert response == False, f"Message: `{message}` may contain adult content"

    def no_bot_content(self):
        for message in self.content_data["Content"]:
            response = self.openai_checker(message, "bot content")
            assert response == False, f"Message: `{message}` may contain bot content"

    def no_long_suspicous_urls(self):
        for message in self.content_data["Content"]:
            response = self.openai_checker(message, "long and suspicious URLs")
            assert (
                response == False
            ), f"Message: `{message}` may contain long and suspicious URLs"

    def no_extremely_negative_sentiment(self):
        for message in self.content_data["Content"]:
            response = self.openai_checker(message, "extremely negative sentiment")
            assert (
                response == False
            ), f"Message: `{message}` may contain extremely negative sentiment"