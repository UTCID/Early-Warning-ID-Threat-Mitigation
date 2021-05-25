from flask import Flask, render_template
from pyattck import Attck
from Combine import get_dictionary
import operator
import json
from scarper import get_rss_feed
attack = Attck()
application = app = Flask(__name__)

final_dictionary, top_mitigation_story = get_dictionary()
dictionary_industry = {}
for k in final_dictionary:
    try:
        if(final_dictionary[k][-1] in dictionary_industry):
            dictionary_industry[final_dictionary[k][-1]] += 1
        else:
            if(final_dictionary[k][-1] == None):
                continue
            dictionary_industry[final_dictionary[k][-1]] = 1
    except Exception as e:
        print(e)
        continue
#print(dictionary_industry)
#print(final_dictionary)

mitigation_information = {}
for mitigation in attack.enterprise.mitigations:
    mitigation_information[mitigation.name] = [mitigation.id, mitigation.description]
#print(mitigation_information)
sector_list = ['Education','Finance','Misc Company','Government', 'Healthcare Industry', 'Retail Shopping', 'Hotels', 'Home Improvement', 'Religious Organization', 'Travel', 'Entertainment', 'Technology']
tactic_frquency = {}
for sector in sector_list:
    temp_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == sector):
            top_tac = final_dictionary[k][0]
            for t in top_tac:
                if(t in temp_dict):
                    temp_dict[t] += 1
                else:
                    temp_dict[t] = 1
    tactic_frquency[sector] = temp_dict
@app.route('/piechart', methods=['GET'])
def pie():
    #blah = {"HealthcareIndustry": 1150, "MiscCompany": 2068, "RetailShopping": 383, "Hotels": 41, "Finance": 391, "HomeImprovement": 79, "Government": 1144, "Technology": 123, "Entertainment": 35, "Education": 379, "ReligiousOrganization": 18, "Travel": 41}
    most_frequent_dict = {}
    for k in tactic_frquency:
        most_frequent_dict[k] = max(tactic_frquency[k].items(), key=operator.itemgetter(1))[0]
    print(most_frequent_dict)
    return render_template('piechart.html', data=dictionary_industry, info = most_frequent_dict )
    #return render_template('piechart.html', data = blah)
@app.route('/EDUCATION')
def education():
    example = {'Story5895': [['Reconnaissance', 'Credential Access', 'Exfiltration'], {'Reconnaissance': ['The adversary is trying to gather information they can use to plan future operations.\n\nReconnaissance consists of techniques that involve adversaries actively or passively gathering information that can be used to support targeting. Such information may include details of the victim organization, infrastructure, or staff/personnel. This information can be leveraged by the adversary to aid in other phases of the adversary lifecycle, such as using gathered information to plan and execute Initial Access, to scope and prioritize post-compromise objectives, or to drive and lead further Reconnaissance efforts.', ['Antivirus/Antimalware', 'Filter Network Traffic', 'Network Intrusion Prevention', 'Pre-compromise', 'Restrict Web-Based Content', 'Spearphishing Attachment Mitigation', 'Spearphishing Link Mitigation', 'User Training']], 'Credential Access': ['The adversary is trying to steal account names and passwords.\n\nCredential Access consists of techniques for stealing credentials like account names and passwords. Techniques used to get credentials include keylogging or credential dumping. Using legitimate credentials can give adversaries access to systems, make them harder to detect, and provide the opportunity to create more accounts to help achieve their goals.', ['Account Use Policies', 'Active Directory Configuration', 'Application Isolation and Sandboxing', 'Audit', 'Bash History Mitigation', 'Brute Force Mitigation', 'Credentials in Files Mitigation', 'Credentials in Registry Mitigation', 'Disable or Remove Feature or Program', 'Encrypt Sensitive Information', 'Exploit Protection', 'Exploitation for Credential Access Mitigation', 'Filter Network Traffic', 'Forced Authentication Mitigation', 'Keychain Mitigation', 'Limit Access to Resource Over Network', 'Multi-factor Authentication', 'Network Intrusion Prevention', 'Network Segmentation', 'Network Sniffing Mitigation', 'Operating System Configuration', 'Password Policies', 'Private Keys Mitigation', 'Privileged Account Management', 'Privileged Process Integrity', 'Restrict File and Directory Permissions', 'Software Configuration', 'Threat Intelligence Program', 'Update Software', 'User Account Management', 'User Training']], 'Exfiltration': ['The adversary is trying to steal data.\n\nExfiltration consists of techniques that adversaries may use to steal data from your network. Once they’ve collected data, adversaries often package it to avoid detection while removing it. This can include compression and encryption. Techniques for getting data out of a target network typically include transferring it over their command and control channel or an alternate channel and may also include putting size limits on the transmission.', ['Automated Exfiltration Mitigation', 'Disable or Remove Feature or Program', 'Encrypt Sensitive Information', 'Exfiltration Over Other Network Medium Mitigation', 'Exfiltration Over Physical Medium Mitigation', 'Filter Network Traffic', 'Limit Hardware Installation', 'Network Intrusion Prevention', 'Network Segmentation', 'Operating System Configuration', 'Password Policies', 'Restrict Web-Based Content', 'Scheduled Transfer Mitigation', 'User Account Management']]}, 'Government']}
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Education"):
            education_dict[k] = final_dictionary[k]

    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)
@app.route('/FINANCE')
def finance():
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Finance"):
            education_dict[k] = final_dictionary[k]
    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)

@app.route('/MISCELLANOUS')
def miscellanous():
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Misc Company"):
            education_dict[k] = final_dictionary[k]
    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)

@app.route('/GOVERNMENT')
def government():
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Government"):
            education_dict[k] = final_dictionary[k]
    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)

@app.route('/HEALTHCARE')
def healthcare():
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Healthcare Industry"):
            education_dict[k] = final_dictionary[k]
    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)

@app.route('/RETAIL')
def retail():
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Retail Shopping"):
            education_dict[k] = final_dictionary[k]
    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)

@app.route('/HOTEL')
def hotel():
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Hotels"):
            education_dict[k] = final_dictionary[k]
    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)

@app.route('/HOME')
def home():
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Home Improvement"):
            education_dict[k] = final_dictionary[k]
    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)

@app.route('/RELIGION')
def religion():
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Religious Organization"):
            education_dict[k] = final_dictionary[k]
    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)

@app.route('/TRAVEL')
def travel():
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Travel"):
            education_dict[k] = final_dictionary[k]
    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)

@app.route('/ENTERTAINMENT')
def entertainment():
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Entertainment"):
            education_dict[k] = final_dictionary[k]
    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)

@app.route('/TECHNOLOGY')
def technology():
    education_dict = {}
    for k in final_dictionary:
        if(final_dictionary[k][-1] == "Technology"):
            education_dict[k] = final_dictionary[k]
    return render_template('Education.html', data = education_dict, info = mitigation_information, mitigation = top_mitigation_story)

@app.route('/CISA')
def cisa_alerts():
    alert_list = get_rss_feed('https://us-cert.cisa.gov/ncas/alerts.xml')
    #print(alert_list)
    return render_template('Cisa.html', data = alert_list)
