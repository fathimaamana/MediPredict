import streamlit as st
import pandas as pd
import re
from datetime import date

from model import predict_health
from remarks import generate_remark

from ai_remarks import generate_ai_remark


from database import (
    insert_patient,
    view_all,
    delete_patient,
    update_patient,
    get_next_patient_id,
    get_patients,
    get_patient_by_id
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="MediPredict",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 MediPredict")
st.subheader("AI-Powered Health Risk Assessment System")

# --------------------------------------------------
# SIDEBAR MENU
# --------------------------------------------------

menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Add Patient",
        "View Patients",
        "Update Patient",
        "Delete Patient"
    ]
)

# ==================================================
# ADD PATIENT
# ==================================================

if menu == "Add Patient":

    st.header("Add New Patient")

    with st.form("patient_form", clear_on_submit=True):

        next_id = get_next_patient_id()

        st.text_input(
            "Patient ID",
            value=f"MED{next_id:03d}",
            disabled=True
        )

        name = st.text_input("Full Name")

        dob = st.date_input(
            "Date of Birth",
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )

        email = st.text_input("Email Address")

        glucose = st.number_input(
            "Glucose",
            min_value=0.0,
            format="%.2f"
        )

        haemoglobin = st.number_input(
            "Haemoglobin",
            min_value=0.0,
            format="%.2f"
        )

        cholesterol = st.number_input(
            "Cholesterol",
            min_value=0.0,
            format="%.2f"
        )

        submitted = st.form_submit_button("Predict and Save")

        if submitted:

            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

            if not name.strip():
                st.error("Name cannot be empty")

            elif not re.match(email_pattern, email):
                st.error("Please enter a valid email address")

            elif glucose <= 0:
                st.error("Glucose must be greater than 0")

            elif haemoglobin <= 0:
                st.error("Haemoglobin must be greater than 0")

            elif cholesterol <= 0:
                st.error("Cholesterol must be greater than 0")

            else:

                risk = predict_health(
                    glucose,
                    haemoglobin,
                    cholesterol
                )

                remark = generate_ai_remark(
                    risk,
                    glucose,
                    haemoglobin,
                    cholesterol
                )

                insert_patient(
                    (
                        name,
                        str(dob),
                        email,
                        glucose,
                        haemoglobin,
                        cholesterol,
                        remark
                    )
                )

                st.success("Patient record saved successfully.")
                st.success(f"Predicted Risk Level: {risk}")
                st.info(remark)

# ==================================================
# VIEW PATIENTS
# ==================================================

elif menu == "View Patients":

    st.header("Patient Records")

    rows = view_all()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "ID",
                "Name",
                "DOB",
                "Email",
                "Glucose",
                "Haemoglobin",
                "Cholesterol",
                "Remarks"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.warning("No patient records found.")

# ==================================================
# UPDATE PATIENT
# ==================================================

elif menu == "Update Patient":

    st.header("Update Patient")

    patients = get_patients()

    if patients:

        patient_options = {
            f"{patient[0]} - {patient[1]}": patient[0]
            for patient in patients
        }

        selected_patient = st.selectbox(
            "Select Patient",
            list(patient_options.keys())
        )

        patient_id = patient_options[selected_patient]

        patient_data = get_patient_by_id(patient_id)

        if patient_data:

            name = st.text_input(
                "Full Name",
                value=patient_data[1]
            )

            dob = st.date_input(
                "Date of Birth",
                value=pd.to_datetime(patient_data[2]).date()
            )

            email = st.text_input(
                "Email Address",
                value=patient_data[3]
            )

            glucose = st.number_input(
                "Glucose",
                value=float(patient_data[4])
            )

            haemoglobin = st.number_input(
                "Haemoglobin",
                value=float(patient_data[5])
            )

            cholesterol = st.number_input(
                "Cholesterol",
                value=float(patient_data[6])
            )

            if st.button("Update Patient"):

                risk = predict_health(
                    glucose,
                    haemoglobin,
                    cholesterol
                )

                remark = generate_ai_remark(
                    risk,
                    glucose,
                    haemoglobin,
                    cholesterol
                )
                
                update_patient(
                    (
                        name,
                        str(dob),
                        email,
                        glucose,
                        haemoglobin,
                        cholesterol,
                        remark,
                        patient_id
                    )
                )

                st.success(
                    "Patient record updated successfully."
                )

    else:

        st.warning(
            "No patients available to update."
        )

# ==================================================
# DELETE PATIENT
# ==================================================

elif menu == "Delete Patient":

    st.header("Delete Patient")

    patients = get_patients()

    if patients:

        patient_options = {
            f"{patient[0]} - {patient[1]}": patient[0]
            for patient in patients
        }

        selected_patient = st.selectbox(
            "Select Patient",
            list(patient_options.keys())
        )

        patient_id = patient_options[selected_patient]

        patient_data = get_patient_by_id(patient_id)

        if patient_data:

            st.text_input(
                "Full Name",
                value=patient_data[1],
                disabled=True
            )

            st.text_input(
                "Email Address",
                value=patient_data[3],
                disabled=True
            )

            st.text_input(
                "Glucose",
                value=str(patient_data[4]),
                disabled=True
            )

            st.text_input(
                "Haemoglobin",
                value=str(patient_data[5]),
                disabled=True
            )

            st.text_input(
                "Cholesterol",
                value=str(patient_data[6]),
                disabled=True
            )

            st.text_area(
                "Remarks",
                value=patient_data[7],
                disabled=True
            )

            confirm = st.checkbox(
                "I confirm that I want to delete this patient record"
            )

            if st.button("Delete Patient"):

                if confirm:

                    delete_patient(patient_id)

                    st.success(
                        "Patient record deleted successfully."
                    )

                    st.rerun()

                else:

                    st.warning(
                        "Please confirm deletion first."
                    )

    else:

        st.warning(
            "No patients available to delete."
        )
# ==================================================
# FOOTER
# ==================================================

st.markdown("---")
st.caption(
    "MediPredict | AI-Powered Health Risk Assessment System"
)