# 代码生成时间: 2025-10-02 02:39:22
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
import pandas as pd
import numpy as np
from typing import Optional

# Pydantic model for input data
class DecisionTreeInput(BaseModel):
    X: list[list[float]] = Field(..., description="Features of the dataset")
    y: list[int] = Field(..., description="Target labels")
    n_estimators: Optional[int] = Field(100, description="Number of tree estimators")
    max_depth: Optional[int] = Field(None, description="Maximum depth of the tree")

# FastAPI app
app = FastAPI()

# Decision tree generator endpoint
@app.post("/decision-tree-generator/")
async def generate_decision_tree(input_data: DecisionTreeInput):
    # Error handling
    if len(input_data.X) == 0 or len(input_data.y) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input data cannot be empty."
        )

    # Split the dataset into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        np.array(input_data.X), np.array(input_data.y), test_size=0.2
    )

    # Initialize the decision tree classifier
    clf = DecisionTreeClassifier(n_estimators=input_data.n_estimators, max_depth=input_data.max_depth)

    # Fit the model
    clf.fit(X_train, y_train)

    # Generate text representation of the decision tree
    decision_tree_text = export_text(clf, feature_names=["f" + str(i) for i in range(len(input_data.X[0]))])

    return {
        "decision_tree": decision_tree_text,
        "n_estimators": clf.n_estimators,
        "max_depth": clf.max_depth
    }

# Error handler for bad requests
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)