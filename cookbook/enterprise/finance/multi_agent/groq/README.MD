# House Bill Analysis with Groq

This project analyzes a House Bill document using the **Groq API** and the **swarms** framework. The document is split into smaller chunks, and each chunk is summarized by three specialized agents: **FinancialStatementsExpert**, **ManagementDiscussionReviewer**, and **RiskAssessmentAnalyst**. The summaries are saved as JSON files, and the progress is logged to allow resuming from the last processed chunk in case of interruptions.

## Prerequisites
- **Python** 3.7+
- **Groq API key**
- Required Python packages: `dotenv`, `groq`, `swarms`, `PyPDF2`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/The-Swarm-Corporation/Cookbook.git
    cd /cookbook/enterprise/finance/multi_agent/groq
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project directory and add your **Groq API key**:
    ```bash
    GROQ_API_KEY=your_groq_api_key
    ```

## Usage

1. **Prepare the House Bill PDF**: Place the House Bill PDF file in the project directory and rename it to `caa.pdf`.

2. **Run the analysis script**:
    ```bash
    python analyze_house_bill_save_progress.py
    ```

   The script will process the document in chunks, summarize each chunk using the three agents, and save the summaries as JSON files. The progress will be logged to `progress.json`.

## How It Works

- **Environment Setup**: The script sets up the environment by loading the Groq API key from the `.env` file and initializing the Groq client.

- **Agent Initialization**: Three specialized agents are initialized:
  - **FinancialStatementsExpert**: Analyzes the financial statements section.
  - **ManagementDiscussionReviewer**: Reviews the management’s discussion and analysis.
  - **RiskAssessmentAnalyst**: Analyzes the risk factors.

- **Workflow Graph**: A workflow graph is created to define the flow of tasks between the agents.

- **Document Processing**:
  - The House Bill PDF is split into smaller chunks.
  - Each chunk is summarized by the three agents.
  - The summaries are saved as JSON files with serialized names indicating the agent and chunk number.
  - The progress is logged to `progress.json`.

- **Rate Limit Handling**: The script ensures that the API calls stay within the specified rate limits (30,000 tokens per minute and 30 requests per minute). If the limits are reached, the script pauses for 60 seconds before continuing.

## Rationale

The rationale behind this approach is to efficiently process a large document by breaking it into manageable chunks and leveraging specialized agents to provide comprehensive summaries. The progress logging ensures that the analysis can be resumed from where it left off in case of interruptions, making the process robust and fault-tolerant.
