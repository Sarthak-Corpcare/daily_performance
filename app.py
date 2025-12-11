import uuid
import tempfile
import streamlit as st
from datetime import datetime

from routes import today_str
from service import excel_processing
from config import SHEETS_TO_IGNORE, LOGO_FILENAME

today_str= datetime.now().strftime("%d-%B-%Y")

st.set_page_config(
    page_title="Daily Performance Processor",
    page_icon="📊",
)

st.title("📊 Daily Performance Excel Processor")
st.write("Upload your raw Daily Performance Excel file")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded_file is not None:
    st.info("File uploaded. Click the button below to process it.")

    if st.button("🚀 Process Excel"):
        with st.spinner("Processing your file..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_input:
                temp_input.write(uploaded_file.getbuffer())
                temp_input_path = temp_input.name

            output_path = f"{tempfile.gettempdir()}/{uuid.uuid4()}.xlsx"

            try:
                
                excel_processing(
                    raw_file=temp_input_path,
                    output_file=output_path,
                    SHEETS_TO_IGNORE=SHEETS_TO_IGNORE,
                    LOGO_FILENAME=LOGO_FILENAME
                )

                with open(output_path, "rb") as f:
                    st.success("Processing complete! Download your file below:")
                    st.download_button(
                        label="📥 Download Daily Performance Report",
                        data=f,
                        file_name=f"Daily Performance Report {today_str}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

            except FileNotFoundError as e:
                st.error(f"Required file not found: {e.filename}. Check your template/config.")
            except Exception as e:

                st.error(f"An error occurred: {e}")
