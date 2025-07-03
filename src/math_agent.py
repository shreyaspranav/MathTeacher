from textwrap import dedent

from typing import Union, TypedDict, List

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import GoogleGenerativeAI

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
        
        # Solution LLM prompt template
        self.solution_prompt_template = PromptTemplate.from_template(
            dedent(
                """
                You are an expert solution writer to math problems.
                
                You are given with a math problem to solve and a similar problem will be given based on 
                the given problem with its solution. Your task is to use the 'guide problem' as an clue
                to solve the given problem.

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
        print(f"This is a query +++++++++++++++++++++++++++++++++++ {query}")
        results = self.math_kb_vectordb.similarity_search_with_relevance_scores(query, k=1)
        print(f"This is fdsajl;fesad;eijfedsa'ijfeausfhds;afdsa {results}")

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
        print("This is a web search")
        state['similar_problem'] = ""
        state['similar_solution'] = ""
        return state
    def _kb_search(self, state: AgentState) -> AgentState:
        print("This is a KB search")
        state['similar_problem'] = ""
        state['similar_solution'] = ""
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
    m = MathAgent(test=1)
    # m.test(prompt='Why does the sum of all angles in a triangle equal to 180')
    m.build_graph()
    result = m.app.invoke({'query': 'What is the integral of x^3'})
    print(result)
        

        
    