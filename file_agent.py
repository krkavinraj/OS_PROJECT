from langchain.agents import AgentExecutor, create_openai_tools_agent
from kavinai.config import llm 
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
load_dotenv()

class FileManagementAgent:
    def __init__(self, root_dir='/Users/kavinraj'):
        self.toolkit = FileManagementToolkit(root_dir=root_dir)
        self.tools = self.toolkit.get_tools()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant capable of managing files and directories.
            You can perform various file management tasks such as creating, deleting, and moving files and directories.
            """),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        self.agent = create_openai_tools_agent(llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def run_file_task(self, task):
        return self.agent_executor.invoke({"input": task})

# Example usage
if __name__ == "__main__":
    agent = FileManagementAgent(root_dir="/Users/kavinraj")
    tasks = [
        "Analyse my files main directory and write me a long summary txt file who am I in kavinAI 1.0.",
    ]

    for task in tasks:
        print(f"\nExecuting task: {task}")
        result = agent.run_file_task(task)
        print(f"Result: {result['output']}")