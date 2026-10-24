# LinkedIn Reflection Workflow

A Python-based AI writing workflow that generates, critiques, and revises Persian LinkedIn posts using the **Reflection Pattern** and the OpenAI-compatible API provided by OpenRouter.

## Overview

This project demonstrates how an LLM can iteratively improve generated content through a three-stage workflow:

1. **Generate:** Create an initial Persian LinkedIn post based on a given topic and tone.
2. **Reflect:** Evaluate the draft and provide actionable feedback.
3. **Revise:** Improve the draft using the reflection feedback.

The project also implements an external feedback mechanism that evaluates objective content constraints using Python, without requiring an additional LLM call.

## Features

- Persian LinkedIn post generation
- Three-stage Reflection workflow
- Configurable topic, tone, and LLM model
- External quality evaluation using Python
- Character-length validation
- Hashtag-count validation
- Comparison between standard reflection and external-feedback reflection
- UTF-8 text output suitable for Persian content
- OpenRouter integration using the OpenAI Python SDK

## Architecture

```text
             Input Topic
                  |
                  v
          +----------------+
          | Generate Draft |
          +----------------+
                  |
                  v
          +----------------+
          | Reflect on     |
          | Draft          |
          +----------------+
                  |
                  v
          +----------------+
          | Revise Draft   |
          +----------------+
                  |
                  v
           Final LinkedIn Post


External Feedback Path
----------------------

          Initial Draft
                  |
                  v
        +-------------------+
        | Quality Checker   |
        | (Python Rules)    |
        +-------------------+
                  |
                  v
          Quality Signals
                  |
                  v
        +-------------------+
        | External Feedback |
        | Reflection        |
        +-------------------+
                  |
                  v
          Detailed Critique
```

## Project Structure

```text
linkedin-reflection/
├── linkedin_workflow.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.12+
- An OpenRouter API key
- An OpenRouter-supported chat model
- Python packages listed in `requirements.txt`

## Installation

### 1. Clone the repository

```bash
git clone https://github.com:akbarmohammadi70/linkedin-reflection-workflow.git
cd linkedin-reflection-workflow
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Keep your API key private. Never commit `.env` to version control.

## Usage

Run the workflow:

```bash
python3.12 ./linkedin_workflow.py
```

The script demonstrates two topics:

- Introducing a new AI and AI Agent training course
- Announcing a professional achievement involving Kubernetes and CI/CD

For each topic, the program displays:

- Initial draft
- Reflection feedback
- Revised LinkedIn post
- Final quality-check results

It then compares standard reflection against reflection augmented with external quality signals.

### Save the output to a text file

Save all terminal output to `output.txt`:

```bash
python3.12 ./linkedin_workflow.py > output.txt
```

Alternatively, display the output in the terminal while saving it:

```bash
python3.12 ./linkedin_workflow.py | tee output.txt
```

## Quality Validation

The `check_post_quality()` function evaluates the generated content using deterministic Python rules.

Default constraints:

| Metric | Requirement |
|---|---|
| Maximum post length | 300 characters |
| Minimum hashtags | 3 |
| Maximum hashtags | 5 |
| External LLM call required | No |

Example:

```python
quality_signals = check_post_quality(
    post_text,
    max_length=300,
    min_hashtags=3,
    max_hashtags=5,
)
```

Example result:

```python
{
    "length": 180,
    "within_length_limit": True,
    "hashtag_count": 0,
    "within_hashtag_range": False
}
```

The values above are illustrative. The function calculates the actual values for the supplied text.

## Reflection vs. External Feedback

The project compares two approaches.

**Standard Reflection**

The LLM evaluates the draft based on its content and the instructions in the prompt.

**External-Feedback Reflection**

A Python function measures the draft and supplies explicit quality signals to the LLM, including the actual character count and hashtag count.

This approach demonstrates an important principle in AI application development: combining language-model reasoning with deterministic validation can make workflows more measurable and easier to evaluate.

## Key Objectives

- Implement the Reflection Pattern in an LLM workflow
- Design structured generation, critique, and revision stages
- Use the OpenAI Python SDK with OpenRouter
- Integrate programmatic validation into an AI workflow
- Compare model-generated feedback with externally measured signals
- Evaluate outputs against explicit constraints

## Limitations

- LLM-generated content is not guaranteed to satisfy all constraints.
- Character and hashtag counts must be checked after revision.
- The current quality checker validates only basic structural requirements.
- Output quality depends on the selected model and prompt design.
- The workflow does not publish posts directly to LinkedIn.

## Future Improvements

- Add an automatic revision loop when quality checks fail.
- Introduce a configurable maximum number of revision attempts.
- Add unit tests for character and hashtag validation.
- Produce structured JSON reports for workflow evaluation.
- Add logging and error handling for API failures.
- Extend validation with readability and content-quality metrics.

## Technologies

- Python 3.12
- OpenRouter API
- OpenAI Python SDK
- python-dotenv
- Large Language Models (LLMs)
- Reflection Pattern
- External Feedback and Rule-Based Validation

## License

This project is intended for educational and experimental purposes. Add a license file if you plan to distribute or reuse the project publicly.
