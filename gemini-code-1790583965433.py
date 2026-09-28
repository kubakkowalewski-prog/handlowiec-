import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Generator Leadów - Odszkodowania", page_icon="⚡", layout="centered")

st.title("⚡ Generator Leadów: Odszkodowania Przesyłowe")
st.markdown("Wprowadź dane nieruchomości oraz oczekiwania klienta, aby wygenerować i zapisać lead sprzedażowy.")

# Formularz wprowadzania danych
with st.form("lead_form"):
    st.subheader("Dane Nieruchomości i Klienta")
    
    col1, col2 = st.columns(2)
    with col1:
        numer_kw = st.text_input("Numer KW (Księgi Wieczystej)", placeholder="np. WA1M/00012345/6")
        numer_dzialki = st.text_input("Numer działki i obręb", placeholder="np. dz. nr 145, obręb Mokotów")
    with col2:
        ilosc_slupow = st.number_input("Ilość słupów na działce", min_value=0, step=1, value=1)
        wartosc_dzialki = st.number_input("Szacowana wartość działki (PLN)", min_value=0.0, step=1000.0, format="%.2f")

    oczekiwania_finansowe = st.number_input("Oczekiwania finansowe klienta (PLN)", min_value=0.0, step=1000.0, format="%.2f")
    
    st.subheader("Kontakt do Klienta")
    imie_nazw = st.text_input("Imię i nazwisko / Nazwa klienta")
    telefon = st.text_input("Numer telefonu")
    
    submitted = st.form_submit_button("💾 Zapisz Lead i Oblicz Szacunek")

if submitted:
    if not numer_kw or not numer_dzialki or not telefon:
        st.error("Proszę uzupełnić przynajmniej numer KW, numer działki oraz telefon kontaktowy!")
    else:
        # Prosta logika szacunkowa (np. orientacyjny potencjalny zwrot bazujący na ilości słupów i wartości)
        szacunkowy_potencjal = ilosc_slupow * 5000.0 # Przykładowa wycena bazowa za słup
        
        nowy_lead = {
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Klient": imie_nazw,
            "Telefon": telefon,
            "Numer KW": numer_kw,
            "Numer Działki": numer_dzialki,
            "Ilość Słupów": ilosc_slupow,
            "Wartość Działki": wartosc_dzialki,
            "Oczekiwania Finansowe": oczekiwania_finansowe,
            "Szacowany Potencjał": szacunkowy_potencjal
        }
        
        # Zapis do pliku CSV (baza danych leada)
        file_path = "leady_odszkodowania.csv"
        df_new = pd.DataFrame([nowy_lead])
        
        if os.path.exists(file_path):
            df_existing = pd.read_csv(file_path)
            df_final = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_final = df_new
            
        df_final.to_csv(file_path, index=False)
        
        st.success("Sukces! Lead został poprawnie zapisany.")
        st.info(f"Szacowany potencjał odszkodowawczy dla {ilosc_slupow} słupów wynosi ok. **{szacunkowy_potencjal:,.2f} PLN**.")

# Panel dla menedżera / podgląd zapisanych leadów
if os.path.exists("leady_odszkodowania.csv"):
    with st.expander("📂 Podgląd zgromadzonych leadów"):
        df_stored = pd.read_csv("leady_odszkodowania.csv")
        st.dataframe(df_stored)
        
        # Opcja pobrania pliku CSV
        csv = df_stored.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Pobierz bazę leadów jako CSV",
            data=csv,
            file_name="leady_odszkodowania.csv",
            mime="text/csv",
        )