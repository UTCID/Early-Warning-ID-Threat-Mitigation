import csv
import re

normalize_dict = {}
normalize_dict = {
    "Broken Into": "Broken Into",
    "Misinformation": "Video Altered",
    "PII/Credential Stolen": ["Stolen", "Leak", "Retained"],
    "Sythentic Information": ["Fraudulent", "Counterfeit", "Falsified", "False", "Fake", "Forged", "Fraud", "Synthetic", "Fabricated"],
    "Impersonation": ["Impersonated", "Posed", "Poses"],
    "Phone Call Scam": ["Phone Call Scam", "Vishing", "SMS Message"],
    "Email Scam": "Email Scam",
    "Access Misuse": ["Misuse", "Inappropriately", "Accessed"],
    "Spear-Phishing": "Spear",
    "Phishing": "Phishing",
    "Security vulnerability/Mismanage": ["Expose", "Carelessly", "Incorrect Address(es)", "Ineligible", "Failed to be Observed", "Misplaced", "Wrong PII", "Default Password", "Mistakingly", "Acccidentally", "Mismanagement", "Unsecured"],
    "Device mishandled": ["Left","Mishandled"],
    "Audio/Visual Involvement": ["Camera", "Video", "Audio", "Viewing"],
    "Removeable Media" :["CD", "USB", "Storage Device" ],
    "Social Media Involvement": ["Twitter", "Facebook", "Social Media"],
    "Malicious Link": "Malicious Link",
    "Malware": "Malware",
    "Ransomeware": ["Ransomware", "Ransome"],
    "DDOS": ["ddos", "Ddos", "DDOS"],
    "Transfer": ["Transferred", "Transfer"]
    }
normalize_org_dict = {
    "Healthcare Industry": ["Health", "Pharmaceuticals", "Healthcare", "Hospital", "Urology", "Medical", "Dental", "Infertility", "Donor", "DentaQuest", "Cardiology", "Recovery", "Heart", "Medicaid", "Visionworks", "Vision",
                            "Joint", "Seton", "Clinic", "Blue Cross", "M.D", "Dr.", "Family Services", "Dermatology", "Surgery", "Aetna", "Life", "MD", "Medicine", "Rehab", "Woman", "Living", "Medicare", "Practice",
                            "Ambulance", "Rehabilitation", "Physician", "Quest", "Blind", "Blood", "Pain", "Cancer", "Disease", "CareFirst", "clinic", "Diagnostics", "Oncology", "Care", "Clinical", "Pfizer", "WakeMed", "Radiology",
                            "Eye", "Ear", "Therapy", "Mental", "Spine", "Pharmacy", "Anesthesia", "Nurse", "Senior", "Medline", "Drug", "Emergency", "Hospice", "Rx", "Optical", "Support", "medical", "BlueShield",
                            "Infants", "LabCorp", "Body", "Allergy", "Counseling", "Omnicare", "Chiropractic", "Red Cross", "Gynecology", "Cosmetic", "Surgical", "Orthopedic", "Dentists", "Dentist", "Insurance",
                            "Meurologic", "Blue", "OB/GYN", "Family", "NHS", "Prescription", "Orthopedics", "Infirmary", "Orthopaedic", "Obamacare", "Skin"],
    "Finance" : ["Life Insurance", "Tax", "tax", "Payroll", "Bank", "bank", "Casino", "MasterCard", "Cash", "Visa", "Document", "Financial", "FileFax", "Chase", "Mortgage", "Fargo", "mortgage", "Credit", "Equifax", "Mutual", "Delloite", "MER"],
    "Retail Shopping": ["Bakery", "Supermarket", "Target", "Price Chopper", "TV", "Coca-Cola", "Costco", "Walmart", "Sam's Club", "Kmart", "FLOWERS", "Flowers", "Grill", "Bar", "Mall", "GameStop", "21", "Food", "HEB", "Wal-Mart",
                        "7-Eleven", "Neiman", "Pizza", "Toys", "Grocery", "Restaurant", "Coffee", "Walgreens", "-", "McDonald's", "Cannibis", "Flower", "CVS", "Cafe", "Store", "Grocers", "Stores", "Gas", "Liquor", "Bread",
                        "Wendy's", "Deli", "Wingstop", "Supply", "Sears", "Buy", "Fabrics", "Shop", "Warehouse", "Farm", "Subs", "Bell", "BBQ", "Chocolate", "Penny", "Dollar", "Starbucks", "Kohls", "Market",
                        "Irish Water"],
    "Hotels": ["Resort", "Airbnb", "Motels", "Hotel", "Tomorrowland", "hotel", "Salon", "Mariott", "Motel"],
    "Home Improvement": ["Home Depot", "Lowes", "Office Depot", "Construction", "Telecom", "AT&T", "Home", "Cricket", "Broadband", "Communications", "Mobile", "Wireless", "Vodafone", "Pest", "Plumbers", "Verizon"],
    "Misc Company": ["unknown", "none", "Law", "Firm", "Unknown", "Sabre", "Power", "Inc.", "LLC", "Partners", "Holdings", "Corporation", "Organization", "FedEx", "Company", "Robotic", "Business",
                    "Club", "Post", "None", "Uknown", "unknown","Varies", "Forbes", "Industries", "Unreported", "Card", "Corp", "Shell", "NONE"],
    "Government": ["Police", "Embassy", "Park", "Department", "Fair", "City", "Specialforces.com", "NYPD", "Detention", "Office", "Patrol", "Courthouse", "Administration", "Interpol", "Highway", "Agency", "Ministry", "DEA",
                    "Authority", "Metropolitan", "Soldier", "Army", "Navy", "U.S.", "Command", "Community", "Division", "County", "United States", "IRS", "FEMA","NASA", "Correctional", "Justice", "Foster", "State", "Internal Revenue",
                    "Passport", "Election", "Case", "Prosecution", "military", "Military", "police", "Services", "Registry", "Security", "Government", "government", "District", "Federal", "Citizens", "Fighters", "Customs", "Town", "Court",
                    "Immigration", "House", "Council", "National", "City", "city", "Mail", "United", "Administration", "Dept.", "Program", "Affairs", "Commission", "Department", "People", "municipal", "Municipal", "Defense", "base",
                    "Base", "Parliment", "Rights", "Minnesota", "state", "Chamber", "Party", "Fort", "Transportation", "DHS", "Board", "DMV", "Planned", "Plant", "Canada", "Prison", "Bureau"],
    "Religious Organization": ["Church", "Mosque", "Temple", "Christian", "St."],
    "Travel": ["Uber", "Boeing", "Air", "Toyota", "Airways", "Metro", "Chevrolet", "Airlines", "Transit", "Nissan", "Travel", "Transport", "Railway", "AIRLINES", "Airlines"],
    "Entertainment": ["Sony", "Entertainment", "Blockbuster", "Disney", "Cable", "Game","Sports", "Theatre", "Theater", "Winery", "Athletics", "Brazzers", "Naughty", "Video", "Nintendo", "Spotify", "Zoo", "Show"],
    "Technology": ["Facebook", "Apple", "Twitter", "Google", ".com", "Venmo", "Yahoo", "Amazon","Microsoft", "Cloudfare", "Adobe", "Paypal", "Technologies", "Technology", "Snapchat", "Netflix", "Automation", "Instagram", "AOL", "Gaana",
                    "Oracle", "Systems", "Software", "IBM"],
    "Education": ["School", "University", "College", "UC", "Library", "Museum", "museum", "High", "university", "Scholarship", "Academy", "ISD", "Art", "Education", "School", "Teachers'","Polytechnic", "District"]
    }
def normalize_input(keyword):
    word = keyword
    for key in normalize_dict:
        try:
            if(normalize_dict[key] in word):
                word = key
        except:
            #for arrays
            for a in normalize_dict[key]:
                if(a in word):
                    word = key
                    break
    return word
def normalize_organization_input(keyword):
    if(len(keyword) == 1 or keyword == "N/A" or len(keyword) == 0 or keyword == "N/a"):
        keyword = "None"
    word = keyword
    for key in normalize_org_dict:
        try:
            if(normalize_org_dict[key] in word):
                word = key
        except:
            #for arrays
            for a in normalize_org_dict[key]:
                if(a in word):
                    word = key
                    break
    final_flag = 0
    for k in normalize_org_dict:
        if(word == k):
            final_flag = 1
    if(final_flag == 0):
        word = "Misc Company"
    return word


def parse_csv():
    file = "ITAP.csv"
    fields = []
    rows = []
    attack_matrix_steps_keywords = {}
    words_avoid = ["FL: ", "Scenario", "Falls Church",
                    "VA: ", "Milwaukee", "WI: ", "Cincinnati", "Texas: ", "OH: ", "Philadelphia", "PA: ", "NY", "NY: ",
                    "PA: ", ]
    with open (file, 'r', encoding = 'utf8') as c_file:
        csvreader = csv.reader(c_file)
        fields = next(csvreader)

        for row in csvreader:
            rows.append(row)
    #print(fields)

    #for r in rows:
        #print (r[6])



    #steps
    attack_matrix_steps_keywords["Reconnaissance"] =  ["Analyze", "Surveil", "Break Into", "Phish", "Misplace", "Mismanage"]
    attack_matrix_steps_keywords["Resource Development"] = ["Impersonate", "Compile", "Lie", "Communicate", "Alter"]
    attack_matrix_steps_keywords["Initial Access"] = ["Send", "Infect", "Acquire", "Mismanage", "Impersonate", "Malfunction", "Misplace", "Communicate","Request" ]
    attack_matrix_steps_keywords["Execution"] =["Breach", "Infect", "Coordinate", "Act Upon", "Ma"]
    attack_matrix_steps_keywords["Persistence"] = ["Abuse", "Create", "Activate"]
    attack_matrix_steps_keywords["Privilege Escalation"]= [ "Abuse"]
    attack_matrix_steps_keywords["Defense Evasion"] = ["Conceal"]
    attack_matrix_steps_keywords["Credential Access"] = ["Steal", "Record"]
    attack_matrix_steps_keywords["Discovery"] = []
    attack_matrix_steps_keywords["Lateral Movement"] = []
    attack_matrix_steps_keywords["Collection"] = [ "Record", "Discover", "Find"]
    attack_matrix_steps_keywords["Command and Control"] = []
    attack_matrix_steps_keywords["Exfiltration"] = ["Upload", "Steal", "Expose", "Inflict Punitive Measure", "Sell", "Transfer", "Leak"]
    attack_matrix_steps_keywords["Impact"] = ["Disable", "Destroy", "Block", "Deactivate", "Send", ",Request"]

    #inputs
    attack_matrix_input_keywords = {}
    attack_matrix_input_keywords["Reconnaissance"] =  ["Broken Into", "Phishing", "Social Media"]
    attack_matrix_input_keywords["Resource Development"] = ["PII/Credential Stolen", "Synthetic Information"]
    attack_matrix_input_keywords["Initial Access"] = ["Sythentic Information", "Device mishandled", "Security vulnerability/Mismanage", "Phishing", "Spear-Phishing", "PII/Credential Stolen"]
    attack_matrix_input_keywords["Execution"] =["Malicious Link", "Malware", "Ransomware"]
    attack_matrix_input_keywords["Persistence"] = ["Access Misue"]
    attack_matrix_input_keywords["Privilege Escalation"]= ["Access Misuse"]
    attack_matrix_input_keywords["Defense Evasion"] = ["Access Misuse"]
    attack_matrix_input_keywords["Credential Access"] = ["Device Mishandled", "Security vulnerability/Mismanage"]
    attack_matrix_input_keywords["Discovery"] = []
    attack_matrix_input_keywords["Lateral Movement"] = []
    attack_matrix_input_keywords["Collection"] = ["Audio/Visual Involvement", "Removeable Media", "Email Scam"]
    attack_matrix_input_keywords["Command and Control"] = []
    attack_matrix_input_keywords["Exfiltration"] = ["Removeable Media", "Transfer"]
    attack_matrix_input_keywords["Impact"] = ["Ransomware", "DDOS", "Misinformation"]

    stories_dict = {}
    for r in rows:
        score = {}
        stories_dict[r[0]] = []
        input = r[6]
        inputs =r[1]
        split_inputs = re.split(",", input)
        #print("STEPS::")
        for s in split_inputs:
            #print(s)
            for k in attack_matrix_steps_keywords:
                if(s in attack_matrix_steps_keywords[k]):
                    #print("\t" + str(k))
                    #print("\t" + str(attack_matrix_steps_keywords[k]))
                    if(k in score):
                        score[k] += 1
                    else:
                        score[k] = 1
                    #print("\t"+str(score))
        #print("INPUTS")
        split_input = re.split(",", inputs)
        for s in split_input:
            if(len(s) == 1):
                continue
            s = normalize_input(s)
            #print(s)
            for k in attack_matrix_input_keywords:
                if(s in attack_matrix_input_keywords[k]):
                    #print("\t" + k)
                    #print("\t" + str(attack_matrix_input_keywords[k]))
                    if(k in score):
                        score[k] += 1
                        if(s == "Audio/Visual Involvement"):
                            score[k] += 1
                    else:
                        score[k] = 1
                        if(s == "Audio/Visual Involvement"):
                            score[k] = 2
        #for k in score:
            #print("\t" + str(k) + ": " + str(score[k]))
                    #print("\t"+str(k))
        org = normalize_organization_input(r[14])
        stories_dict[r[0]].append(score)
        stories_dict[r[0]].append(org)
    return stories_dict

"""
    ###TEMPORARY CODE FOR MANUAL PARSING
    list_orgs = []
    step_words = {}
    inputs_words = {}
    resources_words = {}
    for r in rows:
        steps = r[6]
        inputs = r[1]
        resources = r[5]
        organization = r[14]
        split_steps = re.split(",", steps)
        for s in split_steps:
            if (s in step_words):
                step_words[s] += 1
            else:
                step_words[s] = 1
        split_inputs = re.split(",", inputs)
        for i in split_inputs:
            if(i in inputs_words):
                inputs_words[i] += 1
            else:
                inputs_words[i] = 1
        split_resources = re.split(",", resources)
        for i in split_resources:
            if(i in resources_words):
                resources_words[i] += 1
            else:
                resources_words[i] = 1
        org = normalize_organization_input(organization)
        flag = 0
        for k in normalize_org_dict:
            if(k == org):
                flag = 1
        if(flag == 0 ):
            list_orgs.append(org)

    words_for_matrix_steps = []
    words_for_matrix_inputs = []
    words_for_matrix_resources = []
    flag_bad_word = 0
    for k in step_words:
        flag_bad_word = 0
        for w in words_avoid:
            if(w in k):
                #print(k)
                flag_bad_word = 1
        if(flag_bad_word):
            continue
        words_for_matrix_steps.append(k)
    for k in inputs_words:
        temp_flag = 0
        flag_bad_word = 0
        if(len(k) ==1):
            flag_bad_word = 1
        if(flag_bad_word == 0):
            answer = normalize_input(k)
            for k in normalize_dict:
                if(k == answer):
                    temp_flag = 1
            if(temp_flag ==0):
                words_for_matrix_inputs.append(answer)
    for k in resources_words:
        flag_bad_word = 0
        if(len(k) == 0 or k == "[None Given]"):
            flag_bad_word = 1
        if(flag_bad_word == 0):
            words_for_matrix_resources.append(k)


    #for k in inp
    #print(words_for_matrix_steps)
    #print(len(words_for_matrix_steps))

    print("\n")

    #print(words_for_matrix_inputs)
    #print(len(words_for_matrix_inputs))

    print("\n")
    #print(list_orgs)

    #print(words_for_matrix_resources)
    #print(len(words_for_matrix_resources))
    #####END TEMPORARY CODE
"""
