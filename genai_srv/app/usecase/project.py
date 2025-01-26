from langchain_core.embeddings import Embeddings
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState, END, StateGraph

from app.helpers.chat.message import state_conversation_messages
from app.model.project import Project


DATASET = [
    {
        "task": "Implementacja SSO w Django",
        "description": "Stworzenie systemu logowania z wykorzystaniem Single Sign-On w Django, użycie OAuth2.",
        "estimated_time_hours": 40,
        "actual_time_hours": 45,
        "developer_id": "dev_001",
        "developer_experience": "Expert",
        "skills": [
            {"skill": "Django or id 1", "level": 5},
            {"skill": "OAuth2 or id 33", "level": 4},
            {"skill": "Python or id 44", "level": 5},
            {"skill": "JavaScript", "level": 4},
        ],
    },
    {
        "task": "Stworzenie logowania w React",
        "description": "Stworzenie strony logowania w React, z formularzem do wprowadzania danych.",
        "estimated_time_hours": 15,
        "actual_time_hours": 18,
        "developer_id": "dev_002",
        "developer_experience": "Mid",
        "skills": [
            {"skill": "React", "level": 4},
            {"skill": "JavaScript", "level": 5},
            {"skill": "CSS", "level": 3},
        ],
    },
    {
        "task": "Integracja API z systemem płatności",
        "description": "Integracja z systemem płatności, używając Stripe API do obsługi transakcji.",
        "estimated_time_hours": 30,
        "actual_time_hours": 33,
        "developer_id": "dev_003",
        "developer_experience": "Senior",
        "skills": [
            {"skill": "Python or id 44", "level": 5},
            {"skill": "API Integration", "level": 5},
            {"skill": "Stripe", "level": 4},
            {"skill": "Django", "level": 4},
        ],
    },
]


class EstimateMessagesState(MessagesState):
    document_content: str
    project_tasks: str


class ProjectUseCase:
    def __init__(
        self, model: BaseLanguageModel, embeddings: Embeddings, project: Project
    ) -> None:
        self.model = model
        self.embeddings = embeddings
        self.project = project
        self.graph_builder = StateGraph(EstimateMessagesState)

    async def get_document_content(self, state: EstimateMessagesState):
        return {
            "document_content": f"""
            Title: {self.project.title}
            Content: {self.project.description}
            Complexity: {self.project.complexity}
        """
        }

    async def get_project_tasks(self, state: EstimateMessagesState):
        system_message_content = f"""
            Review the document thoroughly to extract all explicit or implied tasks mentioned and return them as list or nested list.
            
            Here is the document content: {state["document_content"]}
        """
        prompt = [SystemMessage(system_message_content)] + state_conversation_messages(
            state["messages"]
        )
        response = self.model.invoke(prompt)
        return {"project_tasks": response.content}

    async def generate_estimation(self, state: EstimateMessagesState):
        system_message_content = f"""
            Project Estimation Task
            Estimate the time required to complete each task in hours.

            Instructions:
            For each identified task:
            Estimate the number of hours required to complete it.
            If a task is dependent on other tasks, indicate the dependency.
            Summarize all tasks and their estimated durations in a structured format as table.
            All content must be in HTML format. Don't add <html> tag.
            
            Please ensure the estimations are realistic and account for any potential complexities or assumptions. If specific details are unclear, note any assumptions made during the estimation process.

            Estimate this in the Polish language.
            Here is the document tasks: {state["project_tasks"]}
        """
        prompt = [SystemMessage(system_message_content)] + state_conversation_messages(
            state["messages"]
        )
        response = self.model.invoke(prompt)
        return {"messages": [response]}

    async def estimate(self) -> str:
        self.graph_builder.add_node(self.get_document_content)
        self.graph_builder.add_node(self.get_project_tasks)
        self.graph_builder.add_node(self.generate_estimation)

        self.graph_builder.set_entry_point("get_document_content")
        self.graph_builder.add_edge("get_document_content", "get_project_tasks")
        self.graph_builder.add_edge("get_project_tasks", "generate_estimation")
        self.graph_builder.add_edge("generate_estimation", END)

        graph_builder = self.graph_builder.compile()
        response = await graph_builder.ainvoke({"messages": []})
        return response["messages"][-1].content
