from pathlib import Path

from src.foundry_client import (
    ask_foundry,
)

from src.journey import (
    run_complete_journey,
)

from src.services import (
    analyze_document,
    analyze_image,
    analyze_language,
    speech_to_text,
    speech_to_text_microphone,
    translate_text,
)


DATA = (
    Path(__file__).resolve().parent
    / "data"
)


def pause():

    input(
        "\nPress Enter to continue..."
    )


# =========================================================
# LANGUAGE DEMO
# =========================================================

def language_demo():

    text = input(
        "\nEnter English text: "
    ).strip()

    if not text:

        print(
            "No text supplied."
        )

        return

    result = analyze_language(
        text
    )

    print(
        "\nLANGUAGE"
    )

    print(
        "-" * 50
    )

    print(
        "Detected language:",
        result["language"]["name"]
    )

    print(
        "ISO code:",
        result["language"]["iso6391"]
    )

    print(
        "Confidence:",
        result["language"]["confidence"]
    )

    print(
        "\nSentiment:"
    )

    print(
        result["sentiment"]
    )

    print(
        "\nKey phrases:"
    )

    for phrase in (
        result["key_phrases"]
    ):

        print(
            " -",
            phrase
        )

    print(
        "\nEntities:"
    )

    for entity in (
        result["entities"]
    ):

        print(
            f" - {entity['text']} "
            f"({entity['category']})"
        )


# =========================================================
# TRANSLATOR DEMO
# =========================================================

def translator_demo():

    text = input(
        "\nEnter Hindi text "
        "(Enter = sample): "
    ).strip()

    if not text:

        text = (
            DATA /
            "citizen_request_hi.txt"
        ).read_text(
            encoding="utf-8"
        )

    translated = translate_text(
        text,
        source_language="hi",
        target_language="en",
    )

    print(
        "\nTRANSLATION"
    )

    print(
        "-" * 50
    )

    print(
        translated
    )


# =========================================================
# SPEECH DEMO
# =========================================================

def speech_demo():

    print(
        "\nSPEECH"
    )

    print(
        "-" * 50
    )

    print(
        "1. Use microphone"
    )

    print(
        "2. Use WAV file"
    )

    choice = input(
        "Choose: "
    ).strip()

    if choice == "2":

        audio_file = (
            DATA /
            "speech_sample.wav"
        )

        if not audio_file.exists():

            print(
                "\nThe file "
                "data/speech_sample.wav "
                "does not exist."
            )

            print(
                "Add a 16-bit PCM WAV file."
            )

            return

        text = speech_to_text(
            str(audio_file)
        )

    else:

        text = (
            speech_to_text_microphone()
        )

    print(
        "\nSPEECH RESULT"
    )

    print(
        "-" * 50
    )

    print(text)


# =========================================================
# VISION DEMO
# =========================================================

def vision_demo():

    image_file = (
        DATA /
        "driving_license.jpg"
    )

    print(
        "\nAnalyzing:"
    )

    print(
        image_file
    )

    result = analyze_image(
        str(image_file)
    )

    print(
        "\nVISION CAPTION"
    )

    print(
        "-" * 50
    )

    print(
        result["caption"]
    )

    print(
        "\nVISION OCR"
    )

    print(
        "-" * 50
    )

    for line in (
        result["ocr_lines"]
    ):

        print(line)


# =========================================================
# DOCUMENT INTELLIGENCE DEMO
# =========================================================

def document_demo():

    document_file = (
        DATA /
        "citizen_application.pdf"
    )

    print(
        "\nAnalyzing:"
    )

    print(
        document_file
    )

    result = analyze_document(
        str(document_file)
    )

    print(
        "\nDOCUMENT INTELLIGENCE"
    )

    print(
        "-" * 50
    )

    print(
        result["content"]
    )

    if result["tables"]:

        print(
            "\nTABLES"
        )

        for table in (
            result["tables"]
        ):

            print(
                f"{table['row_count']} rows "
                f"x "
                f"{table['column_count']} columns"
            )


# =========================================================
# FOUNDRY MODEL DEMO
# =========================================================

def foundry_demo():

    question = input(
        "\nAsk the Foundry model: "
    ).strip()

    if not question:

        print(
            "No question supplied."
        )

        return

    answer = ask_foundry(
        question
    )

    print(
        "\nFOUNDRY RESPONSE"
    )

    print(
        "-" * 50
    )

    print(answer)


# =========================================================
# MAIN MENU
# =========================================================

def main():

    while True:

        print(
            "\n"
        )

        print(
            "=" * 60
        )

        print(
            " MICROSOFT FOUNDRY"
        )

        print(
            " CITIZEN MULTIMODAL AI ASSISTANT"
        )

        print(
            "=" * 60
        )

        print(
            "1. Language"
        )

        print(
            "2. Translator"
        )

        print(
            "3. Speech"
        )

        print(
            "4. Vision"
        )

        print(
            "5. Document Intelligence"
        )

        print(
            "6. Ask Foundry model"
        )

        print(
            "7. Complete citizen journey"
        )

        print(
            "0. Exit"
        )

        choice = input(
            "\nSelect an option: "
        ).strip()

        try:

            if choice == "1":

                language_demo()
                pause()

            elif choice == "2":

                translator_demo()
                pause()

            elif choice == "3":

                speech_demo()
                pause()

            elif choice == "4":

                vision_demo()
                pause()

            elif choice == "5":

                document_demo()
                pause()

            elif choice == "6":

                foundry_demo()
                pause()

            elif choice == "7":

                run_complete_journey()
                pause()

            elif choice == "0":

                print(
                    "Goodbye."
                )

                break

            else:

                print(
                    "Invalid choice."
                )

        except Exception as exc:

            print(
                "\nERROR"
            )

            print(
                "-" * 50
            )

            print(
                type(exc).__name__
            )

            print(
                exc
            )

            pause()


if __name__ == "__main__":

    main()