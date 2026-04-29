import json
from database import get_connection

DIMENSION_NAMES = [
    "reaction_to_oppression",
    "group_dependency",
    "principle_vs_interest",
    "interpersonal_trust",
    "change_orientation",
    "emotional_stability",
    "core_motivation",
    "historical_mission",
    "response_to_injustice",
    "expression_style"
]

def get_benchmark(era: str = None, region: str = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT f.name, f.era, f.period, p.vector, p.confidence
        FROM figures f
        JOIN profiles p ON f.id = p.figure_id
    """
    
    params = []
    if era:
        if era == "ancient":
            query += " WHERE f.era < 1800"
        elif era == "modern":
            query += " WHERE f.era >= 1800"

    cursor.execute(query, params)
    figures = cursor.fetchall()
    conn.close()

    if not figures:
        return {"error": "No figures found"}

    dimension_sums = [0.0] * 10
    dimension_counts = [0] * 10
    
    for fig in figures:
        vector = json.loads(fig["vector"])
        confidence = json.loads(fig["confidence"])
        
        for i in range(10):
            if confidence[i] >= 0.3:
                dimension_sums[i] += vector[i]
                dimension_counts[i] += 1

    averages = {}
    for i, name in enumerate(DIMENSION_NAMES):
        if dimension_counts[i] > 0:
            averages[name] = round(dimension_sums[i] / dimension_counts[i], 3)
        else:
            averages[name] = None

    high_mission = [f for f in figures 
                   if json.loads(f["vector"])[7] > 0.7]
    high_change = [f for f in figures 
                  if json.loads(f["vector"])[4] > 0.7]
    lone_wolves = [f for f in figures 
                  if json.loads(f["vector"])[1] < 0.3]

    return {
        "total_figures": len(figures),
        "era_filter": era,
        "dimension_averages": averages,
        "insights": {
            "high_mission_driven": len(high_mission),
            "high_change_oriented": len(high_change),
            "lone_wolves": len(lone_wolves)
        }
    }