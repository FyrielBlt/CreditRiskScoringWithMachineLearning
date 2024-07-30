from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import joblib
from category_encoders import OrdinalEncoder, OneHotEncoder
import numpy as np

app = Flask(__name__)

# Chemin vers le modèle
model_path = 'D:/pfe/SCORINGBCM/DATASET/random_forest_modelfr.pkl'

# Charger le modèle
model = joblib.load(model_path)

# Colonnes pour l'encodage et les colonnes sélectionnées
colonnes_one_hot = [
    'TYPEAMORTISSEMENT_', 'GENDAR_', 'SITUATION_FAMILIALE', 'LOCATAIRE', 'DESCRIPTION_CATEGORYENG'
]

colonnes_ordinal = [
    'MATURITECODE_', 'PERIODICITE_CREDIT', 'BIRTHPLACE_',            
    'PROFESSION', 'DISTRICTCODE_', 'DESCRIPTION_TYPEENG',        
    'DESCRIPTION_NATUREENG', 'FINANCIAL_INSTITUTION'
]

selected_columns = [
   'DUREE_CONTRAT', 'TAUXINTERET_',
   'IDINT_', 'NBRPERCH_',
   'Total_MONTANTAGIOS_', 'Total_MONTANTDEBLOCAGE_', 'Total_MONTANTPERTE_',
   'chevauchement_contrat', 'montant_total_credit', 'MONTANT_CREDIT_log',
   'Nombre_Mois_Ouverture_Contrat'
]

# Colonnes attendues par le modèle
expected_columns = [
    'DUREE_CONTRAT', 'MATURITECODE_', 'PERIODICITE_CREDIT', 'TAUXINTERET_',
    'IDINT_', 'BIRTHPLACE_', 'NBRPERCH_', 'PROFESSION', 'DISTRICTCODE_',
    'DESCRIPTION_TYPEENG', 'DESCRIPTION_NATUREENG', 'FINANCIAL_INSTITUTION',
    'Total_MONTANTAGIOS_', 'Total_MONTANTDEBLOCAGE_', 'Total_MONTANTPERTE_',
    'chevauchement_contrat',
    'montant_total_credit', 'MONTANT_CREDIT_log',
    'Nombre_Mois_Ouverture_Contrat', 'TYPEAMORTISSEMENT__Constant',
    'TYPEAMORTISSEMENT__Degressif', 'GENDAR__Femme', 'GENDAR__Homme',
    'SITUATION_FAMILIALE_Celibataire', 'SITUATION_FAMILIALE_Divorce',
    'SITUATION_FAMILIALE_Marie', 'SITUATION_FAMILIALE_Veuf', 'LOCATAIRE_N',
    'LOCATAIRE_O', 'DESCRIPTION_CATEGORYENG_Crédits avec échéanciers',
    'DESCRIPTION_CATEGORYENG_Crédits sans échéanciers',
    'DESCRIPTION_CATEGORYENG_Engagement par signature'
]

# Initialiser les encodeurs
ordinal_encoder = OrdinalEncoder(cols=colonnes_ordinal)
one_hot_encoder = OneHotEncoder(cols=colonnes_one_hot, use_cat_names=True)

# Fonction pour appliquer les encodages aux données
def apply_encodings(data):
    # Sélectionner les colonnes nécessaires pour l'encodage
    data_selected = data[colonnes_one_hot + colonnes_ordinal + selected_columns]

    # Appliquer l'encodage ordinal
    data_encoded_ordinal = ordinal_encoder.fit_transform(data_selected[colonnes_ordinal])
    
    # Appliquer l'encodage one-hot
    data_encoded_one_hot = one_hot_encoder.fit_transform(data_selected[colonnes_one_hot])
        
    # Retirer les colonnes originales qui ont été encodées
    data_remaining = data_selected[selected_columns]
    
    # Combiner les colonnes encodées avec les colonnes restantes
    data_encoded = pd.concat([data_encoded_one_hot, data_encoded_ordinal, data_remaining], axis=1)
    
    # Ajouter les colonnes manquantes avec des valeurs nulles (ou zéro)
    for col in expected_columns:
        if col not in data_encoded.columns:
            data_encoded[col] = 0  # Ajouter des zéros pour les colonnes manquantes
    
    # Réorganiser les colonnes pour correspondre à l'ordre attendu
    data_encoded = data_encoded[expected_columns]
    
    return data_encoded

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home'))

    # Lire le fichier CSV
    data = pd.read_csv(file)

    # Conserver la colonne REFERENCECONTRAT_
    reference_contrat = data['REFERENCECONTRAT_'] if 'REFERENCECONTRAT_' in data.columns else None

    # Appliquer les encodages aux données
    encoded_data = apply_encodings(data)

    # Faire des prédictions avec le modèle
    try:
        predictions = model.predict(encoded_data)
        probabilities = model.predict_proba(encoded_data)
    except ValueError as e:
        print("Erreur:", e)
        print("Colonnes du DataFrame encodé:", encoded_data.columns.tolist())
        return "Une erreur s'est produite lors de la prédiction. Veuillez vérifier les colonnes et réessayer."

    # Ajouter les prédictions et les probabilités à un DataFrame
    results = pd.DataFrame({
        'Prediction': predictions,
        'Probability_DOUTEUSE': probabilities[:, 1],
        'Probability_EN SOUFFRANCE': probabilities[:, 0],
        'Probability_SAINE': probabilities[:, 2]
    })

    # Ajouter la colonne REFERENCECONTRAT_ aux résultats
    if reference_contrat is not None:
        results['REFERENCECONTRAT_'] = reference_contrat

    

    # Déterminer la décision finale
    def decide_final_decision(row):
        if row['Prediction'] == 0 or row['Prediction'] == 1:
            return 'Refusé'
        elif row['Prediction'] == 2:
            if row['Probability_SAINE'] >= 0.40:
                return 'Accepté'
            else:
                return 'Refusé'
        else:
            return 'INCONNU'  # Gérer les cas inattendus

    # Appliquer la fonction de décision finale
    results['Decision Finale'] = results.apply(decide_final_decision, axis=1)

    # Réorganiser les colonnes finales pour l'affichage
    results = results[['REFERENCECONTRAT_', 'Prediction', 'Probability_DOUTEUSE', 'Probability_EN SOUFFRANCE', 'Probability_SAINE', 'Decision Finale']]

    # Retourner les résultats au format HTML
    return render_template('result.html', results=results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
