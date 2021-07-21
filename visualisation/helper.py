import pandas as pd
import xml.etree.ElementTree as ET
import json

def convert_subdomain(input_file):
    sd_content = ""
    with open(input_file) as f:
        sd_content = f.read()
        
    raw_col = []
    for line in sd_content.split("\n"):
        temp_line = line.split(" ")
        domainname = temp_line[0]
        try:
            ips = temp_line[1]
        except:
            ips = ""
        raw_col.append({"domainname":domainname,
                        "ips":ips.split(",")})
    
    df = pd.DataFrame(raw_col)
    df = df.explode("ips")
    
    return df


def convert_list(input_file):
    sd_content = ""
    with open(input_file) as f:
        sd_content = f.read()
        
    output_list = sd_content.split("\n")
    
    return output_list


def convert_nmap_xml(input_file):
    tree = ET.parse(input_file)
    
    parsed_dict_list = []
    new_el = {}

    for node in tree.iter():
        if node.tag == "address":
            if new_el.get("address"):
                parsed_dict_list.append(new_el)
                new_el = {}
            new_el["address"] = node.attrib.get("addr")
        if node.tag == "port":
            if new_el.get("port"):
                parsed_dict_list.append(new_el)
                temp_addr = new_el.get("address")
                new_el = {}
                new_el["address"] = temp_addr
            new_el["port"] = node.attrib.get("portid")
        if node.tag == "state":
            new_el["state"] = node.attrib.get("state")
            new_el["reason"] = node.attrib.get("reason")
            new_el["reason_ttl"] = node.attrib.get("reason_ttl")
        if node.tag == "service":
            new_el["servicename"] = node.attrib.get("name")
            new_el["serviceproduct"] = node.attrib.get("product")
            new_el["serviceversion"] = node.attrib.get("version")
            new_el["serviceinfo"] = node.attrib.get("extrainfo")
            new_el["serviceconf"] = node.attrib.get("conf")

    nmap_df = pd.DataFrame(parsed_dict_list)

    return nmap_df


def unflatten_nuclei_json(input_list):
    for line in input_list:
        if type(line["info"]) == dict:
            for key in line["info"].keys():
                line[key] = line["info"][key]
            del line["info"]
            yield line
        else:
            yield line


def convert_nuclei_to_dataframe(file_path, flatten=True):
    file_output_list = []

    with open(file_path) as f:
        file_output = f.read()

    for line in file_output.split("\n"):
        try:
            file_output_list.append(json.loads(line))
        except Exception as e:
            print(e)
            pass

    df_input_list = []
    if flatten:
        for line in unflatten_nuclei_json(file_output_list):
            df_input_list.append(line)
    nuclei_df = pd.DataFrame(df_input_list)
    return nuclei_df


def convert_curl_output(file_path):

    with open(file_path) as f:
        file_output = f.read() 

    lines = []
    for line in file_output.split("\n"):
        try:
            line_dict = {}
            sp_line = line.split("|")
            line_dict["http_response"] = sp_line[0]
            line_dict["source"] = sp_line[1]
            line_dict["url"]  = sp_line[2]
            line_dict["redir_url"] = sp_line[3]
            line_dict["time_redir"] = sp_line[4]
            line_dict["num_redir"] = sp_line[5]
            line_dict["size_download"] = sp_line[6]
            line_dict["content_type"] = sp_line[7]
            line_dict["filename"] = sp_line[8]
            lines.append(line_dict)
        except:
            pass

    return pd.DataFrame(lines)


def convert_curl_output(file_path):

    with open(file_path) as f:
        file_output = f.read() 

    lines = []
    for line in file_output.split("\n"):
        try:
            line_dict = {}
            sp_line = line.split("|")
            line_dict["http_response"] = sp_line[0]
            line_dict["source"] = sp_line[1]
            line_dict["url"]  = sp_line[2]
            line_dict["redir_url"] = sp_line[3]
            line_dict["time_redir"] = sp_line[4]
            line_dict["num_redir"] = sp_line[5]
            line_dict["size_download"] = sp_line[6]
            line_dict["content_type"] = sp_line[7]
            line_dict["filename"] = sp_line[8]
            lines.append(line_dict)
        except:
            pass

    return pd.DataFrame(lines)