from pathlib import Path

from src.foundry_client import ask_foundry

from src.services import (
    analyze_document,
    analyze_image,
    analyze_language,
    translate_text,
)


DATA = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    / "data"
)


def run_complete_journey():

    hindi_file = (
        DATA /
        "citizen_request_hi.txt"
    )

    image_file = (
        DATA /
        "driving_license.jpg"
    )

    document_file = (
        DATA /
        "citizen_application.pdf"
    )

    # --------------------------------------------
    # 1. CITIZEN REQUEST
    # --------------------------------------------

    hindi_text = (
        hindi_file.read_text(
            encoding="utf-8"
        )
    )

    print(
        "\n1. ORIGINAL CITIZEN REQUEST"
    )

    print(hindi_text)

    # --------------------------------------------
    # 2. TRANSLATION
    # --------------------------------------------

    print(
        "\n2. TRANSLATOR: Hindi -> English"
    )

    english_text = translate_text(
        hindi_text,
        source_language="hi",
        target_language="en",
    )

    print(english_text)

    # --------------------------------------------
    # 3. LANGUAGE
    # --------------------------------------------

    print(
        "\n3. LANGUAGE ANALYSIS"
    )

    language = analyze_language(
        english_text
    )

    print(
        f"Language: "
        f"{language['language']['name']}"
    )

    print(
        f"Sentiment: "
        f"{language['sentiment']['sentiment']}"
    )

    print(
        f"Key phrases: "
        f"{language['key_phrases']}"
    )

    # --------------------------------------------
    # 4. VISION
    # --------------------------------------------

    print(
        "\n4. VISION: DRIVING LICENCE IMAGE"
    )

    vision = analyze_image(
        str(image_file)
    )

    print(
        "Caption:",
        vision["caption"]
    )

    print("OCR:")

    for line in vision["ocr_lines"]:

        print(
            "  ",
            line
        )

    # --------------------------------------------
    # 5. DOCUMENT INTELLIGENCE
    # --------------------------------------------

    print(
        "\n5. DOCUMENT INTELLIGENCE"
    )

    document = analyze_document(
        str(document_file)
    )

    print(
        document["content"]
    )

    # --------------------------------------------
    # 6. FOUNDRY MODEL
    # --------------------------------------------

    context = f"""

You are a citizen services assistant.

Citizen request:

{english_text}


Language analysis:

{language}


Information extracted from the
driving licence image:

{vision}


Information extracted from the
citizen application:

{document["content"]}


Instructions:

Answer the citizen's request clearly.

Use only the information supplied above.

If something is not present,
say that it is not available.

Do not invent government rules,
fees, requirements, or deadlines.

Keep the answer concise and
citizen-friendly.
"""

    print(
        "\n6. FOUNDRY MODEL"
    )

    answer = ask_foundry(
        context
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "FINAL CITIZEN ASSISTANT RESPONSE"
    )

    print(
        "=" * 70
    )

    print(answer)