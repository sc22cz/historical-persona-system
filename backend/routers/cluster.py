import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter(prefix="/cluster", tags=["cluster"])

@router.get("/")
def get_cluster():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.id, f.name, f.era, f.period, p.vector
        FROM figures f
        JOIN profiles p ON f.id = p.figure_id
    """)
    rows = cursor.fetchall()
    conn.close()

    if len(rows) < 5:
        raise HTTPException(status_code=400, detail="Not enough figures for clustering (need at least 5)")

    try:
        import numpy as np
        from sklearn.manifold import TSNE
    except ImportError:
        raise HTTPException(status_code=500, detail="scikit-learn not installed")

    vectors = np.array([json.loads(r["vector"]) for r in rows])

    perplexity = min(30, len(rows) - 1)
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42, n_iter=1000)
    coords = tsne.fit_transform(vectors)

    points = []
    for i, row in enumerate(rows):
        points.append({
            "id": row["id"],
            "name": row["name"],
            "era": row["era"],
            "period": row["period"] or "",
            "x": round(float(coords[i][0]), 3),
            "y": round(float(coords[i][1]), 3),
        })

    return {"points": points, "total": len(points)}
