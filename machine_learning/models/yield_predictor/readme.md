### NB : You have to run ===> *" Yield_predector.ipynb "* to get model's.pkl 


## Difference betwee .pkl and .pt
### *.pkl*

Saves the entire Python object (e.g., a scikit-learn pipeline with preprocessing steps and model).
May include large numpy arrays inefficiently (though joblib is optimized for this).

### *.pt*

Usually stores only the model’s state_dict (weights) by default, not the architecture (unless you save the entire model).
Architecture must be defined separately when loading (unless saved as a full model).