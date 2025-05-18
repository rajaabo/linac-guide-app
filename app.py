# app.py
import streamlit as st
from PIL import Image, ImageDraw
import pandas as pd
import datetime
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Guide LINAC - Installation", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #f4f6fa;
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #0066cc;
    }
    </style>
""", unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["Accueil", "Technicien", "Ingénieur", "Maintenance"],
    icons=["house", "person-badge", "bar-chart", "tools"],
    orientation="horizontal"
)

def init_session():
    if 'etapes' not in st.session_state:
        st.session_state.etapes = {
            "Préparation du site": {"Vérification des dimensions": False},
            "Livraison": {"Inspection": False},
            "Assemblage": {"Montage": False},
            "Installation électrique": {"Branchement": False},
            "Tests": {"Fonctionnement": False},
            "Calibration": {"Alignement": False},
            "Validation finale": {"Contrôle qualité": False}
        }
    if 'problemes' not in st.session_state:
        st.session_state.problemes = []

init_session()

def get_suggestions():
    return {
        "Préparation du site": ["Vérifiez les dimensions de la salle"],
        "Livraison": ["Inspectez les colis avant ouverture"],
        "Assemblage": ["Montez avec précaution selon le manuel"],
        "Installation électrique": ["Coupez l'alimentation avant branchement"],
        "Tests": ["Vérifiez chaque fonction une à une"],
        "Calibration": ["Utilisez des instruments certifiés"],
        "Validation finale": ["Documentez tout le processus"]
    }

suggestions = get_suggestions()

if selected == "Accueil":
    st.markdown('<p class="title">Bienvenue sur le Guide LINAC 🏥</p>', unsafe_allow_html=True)
    st.write("Cette application vous aide à suivre l'installation pas à pas d’un accélérateur linéaire.")

elif selected == "Technicien":
    st.subheader("👷 Interface Technicien")
    technicien = st.text_input("Nom du technicien")
    modele = st.selectbox("Modèle LINAC", ["Elekta", "Varian", "Autre"])

    for etape, sous_etapes in st.session_state.etapes.items():
        with st.expander(etape):
            for sous_etape in sous_etapes:
                st.session_state.etapes[etape][sous_etape] = st.checkbox(sous_etape, value=sous_etapes[sous_etape])
            st.write("💡 Suggestions :")
            for sug in suggestions[etape]:
                st.markdown(f"- {sug}")

elif selected == "Ingénieur":
    st.subheader("📊 Suivi Global")
    total = sum(len(v) for v in st.session_state.etapes.values())
    done = sum(v for d in st.session_state.etapes.values() for v in d.values())
    st.metric("Progression", f"{done}/{total} étapes")
    st.progress(done / total)

elif selected == "Maintenance":
    st.subheader("🛠️ Suivi de Maintenance")
    st.write("Fonctionnalités à venir...")

if st.button("📄 Télécharger rapport PDF"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph("Rapport Installation LINAC", styles['Title']), Spacer(1, 12)]
    for etape, sous in st.session_state.etapes.items():
        story.append(Paragraph(etape, styles['Heading2']))
        for k, v in sous.items():
            story.append(Paragraph(f"{k}: {'✅' if v else '❌'}", styles['Normal']))
    doc.build(story)
    st.download_button("📥 Télécharger le PDF", data=buffer.getvalue(), file_name="rapport_linac.pdf")
