from app.schemas.analysis_result import AnalysisResultCreate
from pydantic import ValidationError
from app.models.analysis_result import AgentName, Labels

def supervisor(model_results : list[AnalysisResultCreate]) -> AnalysisResultCreate:
    final_result = {}
    final_result["upload_id"] = model_results[0].upload_id
    final_result["agent"] = AgentName.SUPERVISOR

    risk_score = []
    confidence = []
    explanation = "Overall assessment:\n"
    evidence = []
    details = {}
    model_version = ""

    confi_label = {
        "manipulated":[],
        "authentic":[],
        "uncertain":[],
    }

    weighted_risk = 0

    for result in model_results:

        risk_score.append(result.risk_score)
        confidence.append(result.confidence)

        weighted_risk += result.risk_score * result.confidence
        explanation += f"\n{result.agent}: \n{result.explanation}"

        evi = {"agent" : result.agent}
        if result.evidence:
            for evid in result.evidence:
                evi.update(evid)
            evidence.append(evi)
        
        if result.details:
            details[result.agent] = result.details
        confi_label[result.label].append(result.confidence)
    

    #risk score
    weighted_risk = (weighted_risk / sum(confidence)) if sum(confidence) != 0 else 0.0
    final_result["risk_score"] = weighted_risk

    #confidence
    for key, values in confi_label.items():
        cnt = len(values)
        confi_label[key] = sum(values)/cnt if cnt != 0 else 0

    #label & confidence

    if 0.0 <= weighted_risk <= 0.30:
        final_result["label"] = Labels.AUTHENTIC
        final_result["confidence"] = confi_label["authentic"]

    elif 0.30 < weighted_risk <= 0.55:
        final_result["label"] =Labels.UNCERTAIN
        final_result["confidence"] = confi_label["uncertain"]
    
    else:
        final_result["label"] = Labels.MANIPULATED
        final_result["confidence"] = confi_label["manipulated"]


    #explanation 
    final_result["explanation"] = explanation

    #evidence
    final_result["evidence"] = evidence if len(evidence)!= 0 else None

    #details
    details["aggregation"] = {
        "method": "confidence_weighted_average",
        "agents_used": len(model_results)
    }
    final_result["details"] = details if len(details) != 0 else None

    try:
        validated_result = AnalysisResultCreate(**final_result)
        return validated_result
    except ValidationError as ve:
        print(f"Does not follow the schema! Problem : {ve} \n")
        raise






    
