from langchain.tools import tool

def create_search_tool(retriever):
    """return a tool function that searches the hr policy document"""

    @tool
    def search_hr_policy(question: str) -> str:
        """search the HR policy document for information about leave, work from home, probation period, notice period, reimbursement policy, code of conduct, holidays or exit process."""
        matching_chunks= retriever.invoke(question)
        return "\n\n".join(chunk.page_content for chunk in matching_chunks)

    return search_hr_policy