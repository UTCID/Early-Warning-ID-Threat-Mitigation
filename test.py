from pyattck import Attck
attack = Attck()
tactic_to_technique_dict = {}
mitigation_to_technique_dict = {}
technique_to_exclude_dict = {}
def create_dicts():
    technique_to_exclude_dict["Reconnaissance"] = []
    technique_to_exclude_dict["Resource Development"] = []
    technique_to_exclude_dict["Initial Access"] = ["Supply Chain Compromise"]
    technique_to_exclude_dict["Execution"] = ["Command and Scripting Interpreter", "Inter-Process Communication", "Native API", "System Services", "Windows Management Instrumentation", "Scheduled Task/Job", "Software Deployment Tools"]
    technique_to_exclude_dict["Persistence"] = ["BITS Jobs", "Boot or Logon Autostart Execution", "Boot or Logon Initialization Scripts", "Compromise Client Software Binary", "Hijack Execution Flow", "Implant Container Image",
                                                "Office Application Startup", "Pre-OS Boot", ""]
    technique_to_exclude_dict["Privilege Escalation"] = ["Access Token Manipulation", "Boot or Logon Autostart Execution", "Boot or Logon Initialization Scripts", "Create or Modify System Process", "Event Triggered Execution",
                                                        "Hijack Execution Flow", "Process Injection"]
    technique_to_exclude_dict["Defense Evasion"] = ["Access Token Manipulation", "BITS Jobs", "Deobfuscate/Decode Files or Information", "Direct Volume Access", "Execution Guardrails", "Hide Artifacts", "Hijack Execution Flow",
                                                    "Indicator Removal on Host", "Indirect Command Execution", "Modify Authentication Process", "Modify Cloud Compute Infrastructure", "Modify Registry",
                                                    "Modify System Image", "Network Boundary Bridging", "Obfuscated Files or Information", "Pre-OS Boot", "Process Injection", "Rogue Domain Controller",
                                                     "Signed Binary Proxy Execution", "Signed Script Proxy Execution", "Subvert Trust Controls", "Trusted Developer Utilities Proxy Execution","Unused/Unsupported Cloud Regions",
                                                     "Virtualization/Sandbox Evasion", "XSL Script Processing" ]
    technique_to_exclude_dict["Credential Access"] = ["OS Credential Dumping", "Steal Application Access Token", "Steal or Forge Kerberos Tickets","Two-Factor Authentication Interception"]
    technique_to_exclude_dict["Discovery"] = ["Application Window Discovery", "Browser Bookmark Discovery", "Cloud Service Dashboard", "Cloud Service Discovery", "Domain Trust Discovery","Network Share Discovery","Network Sniffing",
                                            "Password Policy Discovery", "Peripheral Device Discovery", "Permission Groups Discovery", "Process Discovery", "Query Registry", "Remote System Discovery", "Software Discovery",
                                            "System Information Discovery", "System Network Configuration Discovery", "System Network Connections Discovery", "System Service Discovery", "System Time Discovery", "Virtualization/Sandbox Evasion"]
    technique_to_exclude_dict["Lateral Movement"] = []
    technique_to_exclude_dict["Collection"] = ["Clipboard Data", "Data from Configuration Repository", "Data from Information Repositories", "Data Staged"]
    technique_to_exclude_dict["Command and Control"] = []
    technique_to_exclude_dict["Exfiltration"] = ["Data Transfer Size Limits", "Exfiltration Over C2 Channel"]
    technique_to_exclude_dict["Impact"] = ["Firmware Corruption", "Inhibit System Recovery", "Resource Hijacking", "Service Stop"]
    subtechnique_to_exclude = []
    for technique in attack.enterprise.techniques:
        for k in technique_to_exclude_dict:
            if(technique.name in technique_to_exclude_dict[k]):
                for sub in technique.subtechniques:
                    subtechnique_to_exclude.append(sub.name)
    #print(subtechnique_to_exclude)
    for tactic in attack.enterprise.tactics:
        for technique in tactic.techniques:
            if(technique.name in technique_to_exclude_dict[tactic.name] or technique.name in subtechnique_to_exclude):
                continue
            if(tactic.name in tactic_to_technique_dict):
                tactic_to_technique_dict[tactic.name].append(technique.name)
            else:
                tactic_to_technique_dict[tactic.name] = []
                tactic_to_technique_dict[tactic.name].append(technique.name)
    for mitigation in attack.enterprise.mitigations:
        for technique in mitigation.techniques:
            if(mitigation.name in mitigation_to_technique_dict):
                mitigation_to_technique_dict[mitigation.name].append(technique.name)
            else:
                mitigation_to_technique_dict[mitigation.name] = []
                mitigation_to_technique_dict[mitigation.name].append(technique.name)

def send_dictionary():
    create_dicts()
    return tactic_to_technique_dict, mitigation_to_technique_dict

"""
mitigations_dict = {}
for tactic in attack.enterprise.tactics:
    temp_name_list = []
    #print(tactic.name)
    for tech in tactic.techniques:
        for mitigations in attack.enterprise.mitigations:
            mitigation_techinique_list = []
            for technique in mitigations.techniques:
                mitigation_techinique_list.append(technique.name)
            if(tech.name in mitigation_techinique_list and mitigations.name not in temp_name_list):
                #print("\t" + mitigations.name)
                temp_name_list.append(mitigations.name)
                if(tactic.name in mitigations_dict):
                    mitigations_dict[tactic.name].append(mitigations.name)
                else:
                    mitigations_dict[tactic.name] = []
                    mitigations_dict[tactic.name].append(mitigations.name)
                #print(temp_name_list)
                break
print("Done")
print(mitigations_dict)
"""
