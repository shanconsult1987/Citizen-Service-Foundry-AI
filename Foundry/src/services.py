import json
import uuid

import requests

import azure.cognitiveservices.speech as speechsdk

from azure.ai.textanalytics import TextAnalyticsClient

from azure.ai.vision.imageanalysis import (
    ImageAnalysisClient,
)

from azure.ai.vision.imageanalysis.models import (
    VisualFeatures,
)

from azure.ai.documentintelligence import (
    DocumentIntelligenceClient,
)

from src.auth import (
    get_cognitive_token,
    get_credential,
)

from src.config import (
    FOUNDRY_REGION,
    FOUNDRY_TOOLS_ENDPOINT,
)


def endpoint():

    return FOUNDRY_TOOLS_ENDPOINT.rstrip("/")


# =========================================================
# LANGUAGE
# =========================================================

def analyze_language(text: str) -> dict:

    client = TextAnalyticsClient(
        endpoint=endpoint(),
        credential=get_credential(),
    )

    documents = [text]

    detected = (
        client.detect_language(documents)[0]
    )

    sentiment = (
        client.analyze_sentiment(documents)[0]
    )

    key_phrases = (
        client.extract_key_phrases(documents)[0]
    )

    entities = (
        client.recognize_entities(documents)[0]
    )

    return {
        "language": {
            "name":
                detected.primary_language.name,

            "iso6391":
                detected.primary_language.iso6391_name,

            "confidence":
                detected.primary_language.confidence_score,
        },

        "sentiment": {
            "sentiment":
                sentiment.sentiment,

            "positive":
                sentiment.confidence_scores.positive,

            "neutral":
                sentiment.confidence_scores.neutral,

            "negative":
                sentiment.confidence_scores.negative,
        },

        "key_phrases":
            list(key_phrases.key_phrases),

        "entities": [
            {
                "text": entity.text,

                "category":
                    entity.category,

                "subcategory":
                    entity.subcategory,

                "confidence":
                    entity.confidence_score,
            }

            for entity in entities.entities
        ],
    }


# =========================================================
# TRANSLATOR
# =========================================================

def translate_text(
    text: str,
    source_language: str,
    target_language: str,
) -> str:

    url = (
        f"{endpoint()}/translator/text/v3.0/translate"
        f"?api-version=3.0"
        f"&from={source_language}"
        f"&to={target_language}"
    )

    headers = {
        "Authorization":
            f"Bearer {get_cognitive_token()}",

        "Content-Type":
            "application/json",

        "X-ClientTraceId":
            str(uuid.uuid4()),
    }

    response = requests.post(
        url,
        headers=headers,
        json=[
            {
                "text": text
            }
        ],
        timeout=60,
    )

    response.raise_for_status()

    payload = response.json()

    return (
        payload[0]
        ["translations"][0]
        ["text"]
    )


# =========================================================
# SPEECH
# =========================================================

def create_speech_config(
    language="en-US",
):

    return speechsdk.SpeechConfig(
        token_credential=get_credential(),
        endpoint=endpoint(),
        speech_recognition_language=language,
    )


def speech_to_text_microphone(
    language="en-US",
) -> str:

    speech_config = (
        create_speech_config(language)
    )

    audio_config = (
        speechsdk.audio.AudioConfig(
            use_default_microphone=True
        )
    )

    recognizer = (
        speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
        )
    )

    print(
        "Speak one sentence, then pause..."
    )

    result = recognizer.recognize_once()

    if (
        result.reason
        == speechsdk.ResultReason.RecognizedSpeech
    ):

        return result.text

    if (
        result.reason
        == speechsdk.ResultReason.NoMatch
    ):

        raise RuntimeError(
            "Speech service could not "
            "recognize the audio."
        )

    if (
        result.reason
        == speechsdk.ResultReason.Canceled
    ):

        details = (
            result.cancellation_details
        )

        raise RuntimeError(
            f"Speech recognition canceled: "
            f"{details.reason}. "
            f"{details.error_details or ''}"
        )

    raise RuntimeError(
        f"Unexpected speech result: "
        f"{result.reason}"
    )


def speech_to_text(
    audio_file: str,
    language="en-US",
) -> str:

    speech_config = (
        create_speech_config(language)
    )

    audio_config = (
        speechsdk.audio.AudioConfig(
            filename=str(audio_file)
        )
    )

    recognizer = (
        speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
        )
    )

    result = recognizer.recognize_once()

    if (
        result.reason
        == speechsdk.ResultReason.RecognizedSpeech
    ):

        return result.text

    if (
        result.reason
        == speechsdk.ResultReason.NoMatch
    ):

        raise RuntimeError(
            "Speech service could not "
            "recognize the audio."
        )

    if (
        result.reason
        == speechsdk.ResultReason.Canceled
    ):

        details = (
            result.cancellation_details
        )

        raise RuntimeError(
            f"Speech recognition canceled: "
            f"{details.reason}. "
            f"{details.error_details or ''}"
        )

    raise RuntimeError(
        f"Unexpected speech result: "
        f"{result.reason}"
    )


# =========================================================
# VISION
# =========================================================

def analyze_image(
    image_file: str,
) -> dict:

    client = ImageAnalysisClient(
        endpoint=endpoint(),
        credential=get_credential(),
    )

    with open(
        image_file,
        "rb",
    ) as image_stream:

        image_data = (
            image_stream.read()
        )

    result = client.analyze(
        image_data=image_data,

        visual_features=[
            VisualFeatures.CAPTION,
            VisualFeatures.READ,
        ],
    )

    caption = None

    if result.caption:

        caption = {
            "text":
                result.caption.text,

            "confidence":
                result.caption.confidence,
        }

    lines = []

    if (
        result.read
        and result.read.blocks
    ):

        for block in result.read.blocks:

            for line in block.lines:

                lines.append(
                    line.text
                )

    return {
        "caption": caption,
        "ocr_lines": lines,
    }


# =========================================================
# DOCUMENT INTELLIGENCE
# =========================================================

def analyze_document(
    document_file: str,
) -> dict:

    client = (
        DocumentIntelligenceClient(
            endpoint=endpoint(),
            credential=get_credential(),
        )
    )

    with open(
        document_file,
        "rb",
    ) as document:

        poller = (
            client.begin_analyze_document(
                "prebuilt-layout",
                document,
            )
        )

    result = poller.result()

    pages = []

    for page in result.pages:

        lines = [
            line.content
            for line in (page.lines or [])
        ]

        pages.append(
            {
                "page_number":
                    page.page_number,

                "lines":
                    lines,
            }
        )

    tables = []

    for table in result.tables or []:

        cells = []

        for cell in table.cells:

            cells.append(
                {
                    "row":
                        cell.row_index,

                    "column":
                        cell.column_index,

                    "content":
                        cell.content,
                }
            )

        tables.append(
            {
                "row_count":
                    table.row_count,

                "column_count":
                    table.column_count,

                "cells":
                    cells,
            }
        )

    return {
        "content":
            result.content,

        "pages":
            pages,

        "tables":
            tables,
    }


def compact_json(
    value: dict,
) -> str:

    return json.dumps(
        value,
        indent=2,
        ensure_ascii=False,
    )