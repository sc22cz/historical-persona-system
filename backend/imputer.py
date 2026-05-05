import json
from database import get_connection
from services.matcher import cosine_similarity

def impute_profile(figure_id: int, user_vector: list = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.id, f.name, f.era, p.vector, p.confidence
        FROM figures f
        JOIN profiles p ON f.id = p.figure_id
        WHERE f.id = ?
    """, (figure_id,))

    target = cursor.fetchone()
    if not target:
        return {"error": "Figure not found"}

    target_vector = json.loads(target["vector"])
    target_confidence = json.loads(target["confidence"])

    cursor.execute("""
        SELECT f.id, f.name, f.era, p.vector, p.confidence
        FROM figures f
        JOIN profiles p ON f.id = p.figure_id
        WHERE f.id != ?
    """, (figure_id,))

    modern_figures = cursor.fetchall()
    conn.close()

    imputed_vector = target_vector.copy()
    imputed_from = {}

    for i in range(10):
        if target_confidence[i] < 0.4:
            best_score = -1
            best_figure = None
            best_value = None

            # 从现代人中找最相似的补全
            for fig in modern_figures:
                fig_vector = json.loads(fig["vector"])
                fig_confidence = json.loads(fig["confidence"])

                if fig_confidence[i] >= 0.6:
                    known_dims = [j for j in range(10)
                                  if target_confidence[j] >= 0.5 and fig_confidence[j] >= 0.5]

                    if len(known_dims) >= 3:
                        sim = cosine_similarity(
                            [target_vector[j] for j in known_dims],
                            [fig_vector[j] for j in known_dims]
                        )
                        if sim > best_score:
                            best_score = sim
                            best_figure = fig["name"]
                            best_value = fig_vector[i]

            # 用户向量作为补全来源（如果提供）
            if user_vector is not None:
                known_dims = [j for j in range(10) if target_confidence[j] >= 0.5]
                if len(known_dims) >= 3:
                    sim = cosine_similarity(
                        [target_vector[j] for j in known_dims],
                        [user_vector[j] for j in known_dims]
                    )
                    if sim > best_score:
                        best_score = sim
                        best_figure = "user"
                        best_value = user_vector[i]

            if best_figure:
                imputed_vector[i] = best_value
                imputed_from[i] = {
                    "borrowed_from": best_figure,
                    "similarity": round(best_score, 3)
                }

    return {
        "figure_id": figure_id,
        "original_vector": target_vector,
        "original_confidence": target_confidence,
        "imputed_vector": imputed_vector,
        "imputed_from": imputed_from
    }
