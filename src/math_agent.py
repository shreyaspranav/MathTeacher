import dotenv
from textwrap import dedent

from typing import Union, TypedDict, List

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import GoogleGenerativeAI

from langchain.tools.tavily_search import TavilySearchResults

from langchain.prompts import PromptTemplate

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Config: ---------------------------------------------------------------------------------------------------
model_str = 'gemini-2.0-flash'
temperature = 0.6

similarity_threshold = 0.8


# Implementation of the Math Agent: -------------------------------------------------------------------------

class AgentState(TypedDict):
    query: str
    solution: str
    similar_problem: str
    similar_solution: str

class MathAgent:
    # Private / Protected functions: ----------------------
    def __init__(self, test: Union[str, int]):
        self.llm = GoogleGenerativeAI(model=model_str, temperature=temperature)

        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Load the Chroma vector store from disk
        self.math_kb_vectordb = Chroma(
            persist_directory="./data/math_db",  # same as used during .persist()
            embedding_function=embedding_model
        )

        # Router LLM prompt template
        self.router_prompt_template = PromptTemplate.from_template(
            dedent(
                """
                You are an expert math question similarity checker.
                
                You are given with a math problem and a one possible problem that WE THINK
                is similar. Your job is to analyse both problems and return a "similarity score" on the context
                of math. Remember the way that the similarity score should be determined should be in such a way that
                if the similarity is in a upper threshold, it is safe for an LLM to come up with a solution based on similar
                problem.

                The possible problem that WE THINK is similar might contain the exact keywords but might be completely
                unrelated. So score accordingly to the complete context of the problems. 
                
                Remember: Only return the similarity score ranging from 0 to 100.

                Given Problem: {given_problem}
                Similar Problem: {similar_problem}
                """
            )
        )

        # Setting up Tavily search tool 
        self.search_tool = TavilySearchResults(k=1)
        
        # Solution LLM prompt template
        self.solution_prompt_template = PromptTemplate.from_template(
            dedent(
                """
                You are an expert solution writer to math problems.
                
                You are given with a math problem to solve and a similar problem will be given based on 
                the given problem with its solution. Your task is to use the 'guide problem' as an clue
                to solve the given problem.

                Remember that you should not include any context of the guide problemm in the response.
                It is only for the given for guidance of the problem providing additional context on the problem
                in the hopes of getting an accurate and human friendly solution

                Also make sure that:
                - There is an explanation of the solution as human friendly as possible
                - The solution is formatted such that it is human readable and free of clutter

                Given Problem: {given_problem}
                Guide Problem: {guide_problem}
                Guide Problem's solution: {guide_solution}
                """
            )
        )

    def _router(self, state: AgentState):
        """
        This node routes to either web search or knowledge base search based on the similarlity.
        It also invokes an LLM for secondary verification.
        """

        query = state['query']
        results = self.math_kb_vectordb.similarity_search_with_relevance_scores(query, k=1)

        if results:
            top_doc, top_score = results[0]
            related_question = top_doc.page_content
            related_solution = top_doc.metadata.get('solution', '')
            relation_score = top_score

        if relation_score > similarity_threshold:
            return "kb_search_route"
        else:
            return "web_search_route"
        
    def _web_search(self, state: AgentState) -> AgentState:
        """
        This node retrives the solution of a query by searching the internet.
        """
        
        print("This is a web search")

        # This results in only one result.
        result = self.search_tool.run(state['query'])

        if result[0]['score'] > similarity_threshold:
            state['similar_problem'] = result[0]['title']
            state['similar_solution'] = result[0]['content']
        else:
            # TODO: Choices are: Human in the loop, 
            state['similar_problem'] = ""
            state['similar_solution'] = ""
        return state
    
    def _kb_search(self, state: AgentState) -> AgentState:
        """
        This node retrives the solution of a query by searching the knowledge base vector database.
        """
        print("This is a KB search")

        query = state['query']
        results = self.math_kb_vectordb.similarity_search_with_relevance_scores(query, k=1)

        if results:
            top_doc, top_score = results[0]
            state['similar_problem'] = top_doc.page_content
            state['similar_solution'] = top_doc.metadata['solution']

        return state

    def _solution(self, state: AgentState) -> AgentState:
        """
        This node takes in a similar solution to the query and return the correct answer to it.
        """
        prompt = self.solution_prompt_template.format(
            given_problem = state['query'],
            guide_problem = state['similar_problem'],
            guide_solution = state['similar_solution'],
        )

        state['solution'] = self.llm.invoke(prompt)
        return state

    def build_graph(self):        
        graph = StateGraph(AgentState)

        graph.add_node('router', lambda state: state)
        graph.add_node('web_search', self._web_search)
        graph.add_node('kb_search', self._kb_search)
        graph.add_node('solution', self._solution)

        graph.add_edge(START, 'router')
        graph.add_conditional_edges(
            'router',
            self._router,
            {
                'kb_search_route': 'kb_search',
                'web_search_route': 'web_search'
            }
        )
        graph.add_edge('kb_search', 'solution')
        graph.add_edge('web_search', 'solution')
        graph.add_edge('solution', END)

        self.app = graph.compile()


    def test(self, prompt: str):
        score = self.llm.invoke(self.input_guardrail_prompt.format_messages(user_input=prompt))
        print(score)

    def _input_guardrail(state: AgentState) -> AgentState:
        pass

if __name__ == '__main__':
    dotenv.load_dotenv()
    m = MathAgent(test=1)
    # m.test(prompt='Why does the sum of all angles in a triangle equal to 180')
    m.build_graph()
    result = m.app.invoke({'query': 'What is the integral of x^3'})
    print(result)
        

        
    