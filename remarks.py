def generate_remark(risk):
    if risk == "Low Risk":
        return "Current blood parameters appear stable. Continue maintaining a healthy lifestyle."

    elif risk == "Medium Risk":
        return "Some values require attention. Regular monitoring and lifestyle adjustments are recommended."

    else:
        return "Multiple indicators suggest elevated health risk. Please consult a healthcare professional for further evaluation."