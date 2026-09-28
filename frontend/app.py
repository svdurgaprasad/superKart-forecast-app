
import streamlit as st
import pandas as pd
import requests
from io import BytesIO

BACKEND_URL = os.getenv("API_URL", "http://localhost:7860")

st.set_page_config(page_title="SuperKart Sales Prediction", page_icon="🛒")
st.title("SuperKart Sales Prediction")

# -------------------- Single Prediction --------------------

st.subheader("Single Product Prediction")

product_weight = st.number_input("Product Weight", min_value=0.0, value=10.0)
product_sugar_content = st.selectbox("Product Sugar Content", ["Regular", "Low Sugar", "No Sugar"])
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.0, value=0.05, format="%.3f")
product_mrp = st.number_input("Product MRP", min_value=0.0, value=100.0)
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
product_id_char = st.text_input("Product ID Character", value="FD")
store_age_years = st.number_input("Store Age (Years)", min_value=0, value=10)
product_type_category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

input_data = {
    "Product_Weight": product_weight,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Allocated_Area": product_allocated_area,
    "Product_MRP": product_mrp,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location_city_type,
    "Store_Type": store_type,
    "Product_Id_char": product_id_char,
    "Store_Age_Years": store_age_years,
    "Product_Type_Category": product_type_category
}

if st.button("Predict Sales", type="primary"):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data, timeout=30)
        if response.ok:
            prediction = response.json()["Predicted Sales (in dollars)"]
            st.success(f"Predicted Sales: ${prediction:,.2f}")
        else:
            st.error(f"API error ({response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Unable to connect to prediction API: {e}")


# -------------------- Batch Prediction --------------------

st.divider()
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

if uploaded_file is not None:
    uploaded_file.seek(0)
    st.dataframe(pd.read_csv(uploaded_file), use_container_width=True)

    if st.button("Predict Batch", type="primary"):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files, timeout=60)

            if response.ok:
                predictions_df = pd.read_csv(BytesIO(response.content))
                st.success("Batch predictions completed!")
                st.dataframe(predictions_df, use_container_width=True)
                st.download_button("Download Prediction Results", response.content, "superkart_sales_predictions.csv", "text/csv")
            else:
                st.error(f"API error ({response.status_code}): {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Unable to connect to prediction API: {e}")
