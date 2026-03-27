import shap


def shap_analysis(model, X_test):

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X_test)

    return shap_values