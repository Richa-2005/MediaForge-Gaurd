from app.services.llm.nodes.collect_context import no_analysis_router


def test_graph_aborts_without_analysis_results():
    assert no_analysis_router({"analysis_results": []}) == "Abort"


def test_graph_proceeds_with_primary_analysis():
    state = {
        "analysis_results": [object()],
        "primary_analysis": object(),
    }

    assert no_analysis_router(state) == "Proceed"
