import requests
import json
import re

api_key = 'MCUAgyCvQPONPL9fJismnw'
include = 'all'
clinical_synopsis_categories = ['growth',
                                'growthHeight',
                                'growthWeight',
                                'growthOther',
                                'headAndNeck',
                                'headAndNeckHead',
                                'headAndNeckFace',
                                'headAndNeckEars',
                                'headAndNeckEyes',
                                'headAndNeckNose',
                                'headAndNeckMouth',
                                'headAndNeckTeeth',
                                'headAndNeckNeck',
                                'cardiovascular',
                                'cardiovascularHeart',
                                'cardiovascularVascular',
                                'respiratory',
                                'respiratoryNasopharynx',
                                'respiratoryLarynx',
                                'respiratoryAirways',
                                'respiratoryLung',
                                'chest',
                                'chestExternalFeatures',
                                'chestRibsSternumClaviclesAndScapulae',
                                'chestBreasts',
                                'chestDiaphragm',
                                'abdomen',
                                'abdomenExternalFeatures',
                                'abdomenLiver',
                                'abdomenPancreas',
                                'abdomenBiliaryTract',
                                'abdomenSpleen',
                                'abdomenGastrointestinal',
                                'genitourinary',
                                'genitourinaryExternalGenitaliaMale',
                                'genitourinaryExternalGenitaliaFemale',
                                'genitourinaryInternalGenitaliaMale',
                                'genitourinaryInternalGenitaliaFemale',
                                'genitourinaryKidneys',
                                'genitourinaryUreters',
                                'genitourinaryBladder',
                                'skeletal',
                                'skeletalSkull',
                                'skeletalSpine',
                                'skeletalPelvis',
                                'skeletalLimbs',
                                'skeletalHands',
                                'skeletalFeet',
                                'skinNailsHair',
                                'skinNailsHairSkin',
                                'skinNailsHairSkinHistology',
                                'skinNailsHairSkinElectronMicroscopy',
                                'skinNailsHairNails',
                                'skinNailsHairHair',
                                'muscleSoftTissue',
                                'neurologic',
                                'neurologicCentralNervousSystem',
                                'neurologicPeripheralNervousSystem',
                                'neurologicBehavioralPsychiatricManifestations',
                                'voice',
                                'metabolicFeatures',
                                'endocrineFeatures',
                                'hematology',
                                'immunology',
                                'neoplasia',
                                'prenatalManifestations',
                                'prenatalManifestationsMovement',
                                'prenatalManifestationsAmnioticFluid',
                                'prenatalManifestationsPlacentaAndUmbilicalCord',
                                'prenatalManifestationsMaternal',
                                'prenatalManifestationsDelivery',
                                'laboratoryAbnormalities',
                                'miscellaneous',
                                'molecularBasis']

# Function to fetch a page of results
def fetch_page(start, limit, query):
    # Constructing the URL for the API request
    url = f'https://api.omim.org/api/clinicalSynopsis/search?search={query}&start={start}&limit={limit}&include={include}&format=json&apiKey={api_key}'
    
    # Making the GET request to the OMIM API
    response = requests.get(url)
    
    # Checking if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data from OMIM API, status code: {response.status_code}")
        return []
    return response.json()['omim']['searchResponse']['clinicalSynopsisList']

def clean_text(text):
    # Remove anything in parentheses or curly braces or square brackets
    pattern = r'\{[^}]*\}|\([^)]*\)|\[[^\]]*\]'
    # Replace found patterns with an empty string
    cleaned_text = re.sub(pattern, '', text)
    # Remove any additional, unnecessary spaces that may have been left over
    cleaned_text = re.sub(' +', ' ', cleaned_text).strip()

    # Remove trailing punctuation
    cleaned_text = cleaned_text.rstrip(';')
    cleaned_text = cleaned_text.rstrip(',')
    cleaned_text = cleaned_text.rstrip('.')

    return cleaned_text.strip()


def clean_list(text_list):
    return [clean_text(text) for text in text_list]

if __name__ == '__main__':
    query = 'epilepsy'
    start = 0
    limit = 20

    # Collect all entries
    all_entries = []
    while True:
        page_entries = fetch_page(start, limit, query)
        if not page_entries:
            break
        all_entries.extend(page_entries)
        start += limit

    query = 'seizures'
    start = 0

    while True:
        page_entries = fetch_page(start, limit, query)
        if not page_entries:
            break
        all_entries.extend(page_entries)
        start += limit
    
    modified_clinical_entries = []
    for entry in all_entries:
        d = {}
        clincial_data = entry['clinicalSynopsis']
        d['mimNumber'] = clincial_data['mimNumber']
        d['preferredTitle'] = clincial_data['preferredTitle']
        clinical_synopsis_list = []
        for category in clinical_synopsis_categories:
            if category not in clincial_data:
                continue
            data = clincial_data[category]
            
            # Split by semicolon
            data = data.split(";")
            
            for symptom in data:
                # Clean the text
                symptom = clean_text(symptom)
                if len(symptom) > 0:
                    clinical_synopsis_list.append(symptom)
        d['clinicalSynopsis'] = clinical_synopsis_list
        modified_clinical_entries.append(d)

    f = open("seizure_epilepsy.json", "w")
    json.dump(modified_clinical_entries, f, indent=4)