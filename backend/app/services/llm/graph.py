from app.services.llm.nodes.collect_context import collect_context,no_analysis_router
from app.services.llm.nodes.explain import explain
from app.services.llm.nodes.format_markdown import format_markdown
from app.services.llm.nodes.persist import persist
from app.services.llm.state import ExplanationState

from langgraph.graph import StateGraph, START, END

graph = StateGraph(ExplanationState)

graph.add_node("context",collect_context)
graph.add_node("explain",explain)
graph.add_node("format_markdown",format_markdown)
graph.add_node("persist",persist)

graph.add_edge(START, "context")
graph.add_conditional_edges(
    "context",
    no_analysis_router,
    {
        "Proceed": "explain",
        "Abort": END,
    },
)

graph.add_edge("explain","format_markdown")
graph.add_edge("format_markdown","persist")
graph.add_edge("persist",END)

explanation_graph = graph.compile()



