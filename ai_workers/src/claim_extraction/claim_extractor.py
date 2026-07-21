import spacy


class ClaimExtractor:
    """
    Extracts objective factual claims from raw text.

    Filters out:
    - greetings
    - questions
    - opinions
    - speculation
    - commands
    - sentence fragments
    """

    MIN_WORDS = 3

    SUBJECTIVE_PHRASES = {
        "i think",
        "i believe",
        "i feel",
        "personally",
        "in my opinion",
        "we think",
        "we believe",
    }

    SPECULATIVE_PHRASES = {
        "maybe",
        "perhaps",
        "probably",
        "possibly",
        "likely",
        "apparently",
        "could be",
        "might be",
        "it seems",
        "seems",
    }

    GREETINGS = {
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "thanks",
        "thank you",
    }

    SUBJECTIVE_ADJECTIVES = {
        "best",
        "worst",
        "amazing",
        "awesome",
        "great",
        "terrible",
        "excellent",
        "fantastic",
        "beautiful",
        "wonderful",
        "perfect",
        "horrible",
    }

    VALID_ENTITY_LABELS = {
        "PERSON",
        "ORG",
        "GPE",
        "LOC",
        "PRODUCT",
        "EVENT",
        "LAW",
        "FAC",
        "NORP",
        "DATE",
    }

    INVALID_SUBJECTS = {
        "i",
        "you",
        "we",
        "he",
        "she",
        "they",
        "it",
        "this",
        "that",
        "these",
        "those",
    }

    def __init__(self):

        self.nlp = spacy.load("en_core_web_sm")

    def extract(
        self,
        text: str,
    ) -> list[str]:

        doc = self.nlp(text)

        claims = []

        for sent in doc.sents:

            sentence = sent.text.strip()

            if self.is_valid_claim(
                sentence,
                sent,
            ):
                claims.append(sentence)

        return claims

    def is_valid_claim(
        self,
        sentence: str,
        span,
    ) -> bool:

        if not sentence:
            return False

        if len(sentence.split()) < self.MIN_WORDS:
            return False

        if self.is_question(sentence):
            return False

        if self.is_greeting(sentence):
            return False

        if self.is_subjective(sentence):
            return False

        if self.is_speculative(sentence):
            return False

        if self.contains_subjective_adjective(span):
            return False

        if self.is_imperative(span):
            return False

        if not self.has_subject(span):
            return False

        if not self.has_verb(span):
            return False

        # Accept either:
        # 1. Named entities
        # 2. Scientific/general factual subjects
        if not (
            self.has_named_entity(span)
            or self.has_meaningful_subject(span)
        ):
            return False

        return True

    def is_question(
        self,
        sentence: str,
    ) -> bool:

        return sentence.endswith("?")

    def is_subjective(
        self,
        sentence: str,
    ) -> bool:

        sentence = sentence.lower()

        return any(
            phrase in sentence
            for phrase in self.SUBJECTIVE_PHRASES
        )

    def is_speculative(
        self,
        sentence: str,
    ) -> bool:

        sentence = sentence.lower()

        return any(
            phrase in sentence
            for phrase in self.SPECULATIVE_PHRASES
        )

    def is_greeting(
        self,
        sentence: str,
    ) -> bool:

        sentence = sentence.lower()

        return any(
            sentence.startswith(greeting)
            for greeting in self.GREETINGS
        )

    def has_subject(
        self,
        span,
    ) -> bool:

        return any(
            token.dep_ in (
                "nsubj",
                "nsubjpass",
            )
            for token in span
        )

    def has_verb(
        self,
        span,
    ) -> bool:

        return any(
            token.pos_ in (
                "VERB",
                "AUX",
            )
            for token in span
        )

    def has_named_entity(
        self,
        span,
    ) -> bool:

        return any(
            ent.label_ in self.VALID_ENTITY_LABELS
            for ent in span.ents
        )

    def has_meaningful_subject(
        self,
        span,
    ) -> bool:
        """
        Accept scientific/general factual statements
        even if no Named Entity exists.

        Example:
            Water boils at 100°C.
            Hydrogen is the lightest element.
            Photosynthesis converts sunlight.
        """

        for token in span:

            if token.dep_ in (
                "nsubj",
                "nsubjpass",
            ):

                if token.pos_ in (
                    "NOUN",
                    "PROPN",
                ):

                    if (
                        token.text.lower()
                        not in self.INVALID_SUBJECTS
                    ):

                        return True

        return False

    def contains_subjective_adjective(
        self,
        span,
    ) -> bool:
        """
        Reject statements that rely on subjective adjectives.

        Example:
            Apple is amazing.
            Pizza tastes great.
        """

        for token in span:

            if (
                token.pos_ == "ADJ"
                and token.lemma_.lower()
                in self.SUBJECTIVE_ADJECTIVES
            ):
                return True

        return False

    def is_imperative(
        self,
        span,
    ) -> bool:
        """
        Detect simple commands.

        Example:
            Subscribe now.
            Click here.
            Open the file.
        """

        if not span:
            return False

        first = span[0]

        return (
            first.pos_ in ("VERB", "AUX")
            and first.dep_ == "ROOT"
        )


if __name__ == "__main__":

    sample = """
    Hello everyone.

    India has 28 states.

    Earth is flat.

    Water boils at 100 degrees Celsius.

    Hydrogen is the lightest element.

    WHO declared COVID-19 a pandemic.

    The Eiffel Tower is located in Paris.

    I think Apple makes the best phones.

    Apple is amazing.

    Maybe the election was rigged.

    Can humans live on Mars?

    Subscribe to this channel.

    Gravity attracts objects toward Earth.

    Photosynthesis converts sunlight into chemical energy.
    """

    extractor = ClaimExtractor()

    claims = extractor.extract(sample)

    print("\nExtracted Claims\n")

    for claim in claims:
        print("-", claim)