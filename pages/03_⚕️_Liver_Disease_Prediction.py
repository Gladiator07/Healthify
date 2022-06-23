import config as cfg
import joblib
import numpy as np
import streamlit as st


def doctor_search(doctor_type):
    """
    Searches the specialist near you
    """
    base_url = "https://www.google.com/search?q="
    query = doctor_type.split(" ")
    query = "+".join(query)
    query = f"{query}+near+me"
    final_url = base_url + query

    return final_url


def liver_app():
    st.title("Liver Disease Diagnosis")

    st.subheader(
        "Enter the details from the patients report to check the chance of liver disease"
    )

    model = joblib.load(cfg.LIVER_MODEL)

    gender = st.radio("Gender", ("Male", "Female"))

    if gender == "Male":
        gender = 1
    else:
        gender = 0
    age = st.slider("Age", min_value=1, max_value=110)

    total_bilirubin = st.slider(
        "Total Bilirubin (in mg/dL)", min_value=0.1, max_value=40.0
    )

    direct_bilirubin = st.slider("Direct Bilirubin (in mg/dL)")

    alk_phosphate = st.slider(
        "Alkaline Phosphotase (in units/L", min_value=10, max_value=250
    )

    alamine_aminotransferase = st.slider(
        "Alamine Aminotransferase (in units/L)", min_value=20, max_value=120
    )

    aspartate_aminotransferase = st.slider(
        "Aspartate Aminotransferase (in units/L)", min_value=20, max_value=140
    )

    total_proteins = st.slider(
        "Total Proteins (in g/dL)", min_value=2.0, max_value=10.0, step=0.1
    )

    albumin = st.slider("Albumin (in g/dL)", min_value=1.0, max_value=10.0, step=0.1)

    ratio = st.slider(
        "Albumin and Globulin Ratio", min_value=0.1, max_value=3.0, step=0.01
    )

    inp_array = np.array(
        [
            [
                age,
                gender,
                total_bilirubin,
                direct_bilirubin,
                alk_phosphate,
                alamine_aminotransferase,
                aspartate_aminotransferase,
                total_proteins,
                albumin,
                ratio,
            ]
        ]
    )

    predict = st.button("Predict")
    if predict:
        liver_disease_prob = model.predict(inp_array)

        if liver_disease_prob == 1:
            st.subheader("The patient have chances of having a liver disease 😔")
            pcp = doctor_search("Primary Care Provider")
            gastro = doctor_search("Gastroenterologists")
            st.subheader(
                "Please consult with your family doctor or one of the below doctors immediately"
            )

            st.write(
                "Click on the specialists to get the specialists nearest to your location 📍"
            )
            st.markdown(f"- [Primary Care Doctor]({pcp}) 👨‍⚕")
            st.markdown(f"- [Gastroenterologists]({gastro}) 👨‍⚕")
        if liver_disease_prob == 2:

            st.subheader(
                "The patient doesn't have any chances of having a liver disease 😄"
            )

            st.balloons()


if __name__ == "__main__":
    liver_app()
