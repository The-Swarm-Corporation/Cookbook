import os
WORKSPACE_DIR = "C:/swarms-groq"
os.environ["WORKSPACE_DIR"] = WORKSPACE_DIR
from dotenv import load_dotenv
from groq import Groq
from swarms import Agent, GraphWorkflow, Node, NodeType, Edge
import PyPDF2
import time
import json

# Load environment variables
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("GROQ_API_KEY")
if api_key is None:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

# Initialize Groq 
client = Groq(api_key=api_key)

print("Environment set up and model initialized successfully!")

# Step 2: Creating the Agents
# Define function to make the agent response
def create_agent_response(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "you are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# Initialize FinancialStatementsExpert agent
financial_statements_expert = Agent(
    agent_name="FinancialStatementsExpert",
    llm=create_agent_response,
    max_loops=1,
    autosave=True,
    dashboard=False,
    system_prompt=(
        "You are an expert in financial analysis. Your task is to thoroughly analyze the financial statements section "
        "of the CAA Act. Pay close attention to the budget allocations, expenditures, and financial implications. Identify "
        "key financial metrics such as funding distribution, spending efficiency, and financial sustainability. Provide a detailed "
        "summary of your findings, highlighting any potential red flags or areas of concern."
    )
)

# Initialize ManagementDiscussionReviewer agent
management_discussion_reviewer = Agent(
    agent_name="ManagementDiscussionReviewer",
    llm=create_agent_response,
    max_loops=1,
    autosave=True,
    dashboard=False,
    system_prompt=(
        "You specialize in understanding and interpreting management's discussion and analysis. Your task is to critically "
        "review the strategic decisions and discussions in Part 1 of the CAA Act. Identify key themes such as policy objectives, "
        "strategic initiatives, and forward-looking statements. Analyze the tone and language used to assess confidence in the "
        "implementation of the Act. Summarize the key points and provide insights into potential risks or opportunities."
    )
)

# Initialize RiskAssessmentAnalyst agent
risk_assessment_analyst = Agent(
    agent_name="RiskAssessmentAnalyst",
    llm=create_agent_response,
    max_loops=1,
    autosave=True,
    dashboard=False,
    system_prompt=(
        "As an expert in risk management, your task is to analyze the risk factors associated with Part 1 of the CAA Act. Carefully read through "
        "the identified risks, and assess their potential impact on the Act's implementation and financial performance. Prioritize the risks based "
        "on their severity and likelihood, and provide recommendations on how these risks might be mitigated."
    )
)

print("Agents created successfully!")

# Step 3: Building the Workflow Graph
# Define a sample task function
def sample_task():
    print("Running sample task")
    return "Task completed"

# Initialize the workflow graph
wf_graph = GraphWorkflow()

# Add nodes for each agent
wf_graph.add_node(Node(id="financial_statements_expert", type=NodeType.AGENT, agent=financial_statements_expert))
wf_graph.add_node(Node(id="management_discussion_reviewer", type=NodeType.AGENT, agent=management_discussion_reviewer))
wf_graph.add_node(Node(id="risk_assessment_analyst", type=NodeType.AGENT, agent=risk_assessment_analyst))

# Add a sample task node
wf_graph.add_node(Node(id="task1", type=NodeType.TASK, callable=sample_task))

# Define the edges (flow of tasks)
wf_graph.add_edge(Edge(source="financial_statements_expert", target="task1"))
wf_graph.add_edge(Edge(source="management_discussion_reviewer", target="task1"))
wf_graph.add_edge(Edge(source="risk_assessment_analyst", target="task1"))

# Set entry and end points for the workflow
wf_graph.set_entry_points(["financial_statements_expert", "management_discussion_reviewer", "risk_assessment_analyst"])
wf_graph.set_end_points(["task1"])

# Visualize the workflow
print(wf_graph.visualize())

print("Workflow graph created successfully!")

# Step 4: Running the Workflow
def load_pdf_to_string(file_path: str, start_page: int, end_page: int):
    # Open the PDF file in read-binary mode
    with open(file_path, 'rb') as file:
        # Create a PDF file reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        text = ""
        # Loop through the specified range of pages and extract text
        for page_number in range(start_page, end_page):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()
        
        # Return the extracted text
        return text

def split_text_into_chunks(text: str, max_tokens: int):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def summarize_text(agent_name: str, text: str):
    summary_prompt = f"Summarize the following text within 950 tokens:\n\n{text}"
    return create_agent_response(summary_prompt)

def process_chunks(chunks):
    tokens_used = 0
    requests_made = 0

    for i, chunk in enumerate(chunks):
        if tokens_used + len(chunk.split()) > 30000 or requests_made >= 30:
            print("Rate limit reached. Waiting for 60 seconds...")
            time.sleep(60)
            tokens_used = 0
            requests_made = 0

        # Process each agent separately and serialize outputs with numbers
        for agent_name in ["financial_statements_expert", "management_discussion_reviewer", "risk_assessment_analyst"]:
            summarized_chunk = summarize_text(agent_name, chunk)
            
            # Save the summarized chunk to a JSON file with agent name included
            file_name = f"{agent_name}_summary_chunk_{i+1}.json"
            with open(file_name, 'w') as f:
                json.dump(summarized_chunk, f)
            
            print(f"{agent_name} summary for chunk {i+1}: {summarized_chunk}")
            
            tokens_used += len(chunk.split())
            requests_made += 1

# Load the CAA Act summary in chunks
file_path = "C:/swarms-groq/caa.pdf"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

# Define the chunk size (number of pages per chunk)
chunk_size = 5  # Adjusted to ensure smaller chunks that fit within token limits
num_pages = len(PyPDF2.PdfReader(open(file_path, 'rb')).pages)

all_chunks = []
for start_page in range(0, num_pages, chunk_size):
    end_page = min(start_page + chunk_size, num_pages)
    caa_summary_chunk = load_pdf_to_string(file_path, start_page, end_page)
    text_chunks = split_text_into_chunks(caa_summary_chunk, max_tokens=500)
    all_chunks.extend(text_chunks)

process_chunks(all_chunks)

print("Execution completed successfully!")