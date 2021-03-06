from IPython.display import IFrame
import json
import os
import uuid

def vis_network(nodes, edges, physics=False, res=False, hierarchical=False, physics_model="hierarchicalRepulsion"):
    physical_dict = {       
        "hierarchicalRepulsion":"""
              physics: {{
              enabled: {physics},
              hierarchicalRepulsion: {{
                  centralGravity: 0,
                  nodeDistance: 390,
                  springLength: 900,
                  springConstant: 0.96,
                  damping: 0.8,
               }},
              minVelocity: 0.01,
              maxVelocity: 9,
              solver: "hierarchicalRepulsion"
          }}
    """,
        "forcedAtlas2Based":"""
              physics: {{
              enabled: {physics},
              forcedAtlas2Based: {{
                  centralGravity: 0,
                  gravitationalConstant: 0,
                  springLength: 900,
                  springConstant: 0.195,
                  avoidOverlap: 0.96,
                  damping: 0.8,
               }},
              minVelocity: 0.01,
              maxVelocity: 9,
              solver: "forceAtlas2Based"
          }}
    """,
        "barnesHut":"""
              physics: {{
              enabled: {physics},
              barnesHut: {{
                  centralGravity: 0,
                  gravitationalConstant: -15150,
                  springLength: 460,
                  springConstant: 0.195,
                  avoidOverlap: 0.96,
                  damping: 0.8,
               }},
              minVelocity: 0.75
          }}
    
    """
    }
    
    if hierarchical:
        hierarchical_text = """
        layout: {{
          hierarchical: {{
            direction: "LR",
            levelSeperation: 20000,
          }},
        }},
        """
    else:
        hierarchical_text = ""
    
    if res:
        res_js = "http://127.0.0.1/res/vis.min.js"
        res_css = "http://127.0.0.1/res/vis.min.css"
    else:
        res_js = "https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"
        res_css = "https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css"
    
    html = """
    <html>
    <head>
      <script type="text/javascript" src="""+res_js+"""></script>
      <link href="""+res_css+""" rel="stylesheet" type="text/css">
    </head>
    <body>
    <div id="{id}"></div>
    <script type="text/javascript">
      var nodes = new vis.DataSet({nodes});
      var edges = {edges};
      var container = document.getElementById("{id}");
      var data = {{
        nodes: nodes,
        edges: edges
      }};
      var options = {{
      """+hierarchical_text+"""
          nodes: {{
              shape: 'dot',
              size: 25,
              font: {{
                  size: 14
              }}
          }},
              
          edges: {{
              font: {{
                  size: 14,
                  align: 'middle'
              }},
              color: {{
                  inherit: false
              }},
              arrows: {{
                  to: {{enabled: true, scaleFactor: 0.5}}
              }},
              smooth: {{type: "horizontal"}}
          }},
          """+physical_dict[physics_model]+"""
      }};
      var network = new vis.Network(container, data, options);
    </script>
    </body>
    </html>
    """

   
    
    unique_id = str(uuid.uuid4())
    html = html.format(id=unique_id, nodes=json.dumps(nodes), edges=json.dumps(edges), physics=json.dumps(physics))

    filename = "figure/graph-{}.html".format(unique_id)

    file = open(filename, "w")
    file.write(html)
    file.close()
    
    download_link = os.getcwd().replace("/workspace","http://127.0.0.1:8080/files") + "/" + filename

    return IFrame(filename, width="100%", height="400"), download_link

def draw(graph, physics=False, hierarchical=False, res=False,limit=10000, physics_model=""):
    # The options argument should be a dictionary of node labels and property keys; it determines which property
    # is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
    # Omitting a node label from the options dict will leave the node unlabeled in the visualization.
    # Setting physics = True makes the nodes bounce around when you touch them!
    query = """
    MATCH (n)
    WITH n, rand() AS random
    ORDER BY random
    LIMIT $limit
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n AS source_node,
           id(n) AS source_id,
           r,
           m AS target_node,
           id(m) AS target_id
    """

    data = graph.run(query, limit=limit)

    nodes = []
    edges = []

    def get_vis_info(node, id):
        node_type = list(node.labels)[0]
        node_size = node.get("label")
        if node_size:
            node_size = int(node_size)*3 + 25
        else:
            node_size = 25
        vis_label = node["name"]
        try:
            title = node["description"]
        except:
            title = ""
        color = node["color"]

        return {"id": id, "label": vis_label, "group": node_type, "size": node_size, "title": title, "color": color}

    
    for row in data:
        source_node = row[0]
        source_id = row[1]
        rel = row[2]
        target_node = row[3]
        target_id = row[4]

        source_info = get_vis_info(source_node, source_id)

        if source_info not in nodes:
            nodes.append(source_info)
            
        if rel is not None:
            target_info = get_vis_info(target_node, target_id)

            if target_info not in nodes:
                nodes.append(target_info)
                
            # color map for nmap portscans
            color_map = {'open': "#00ff00",'filtered': "#ff0000", '400': "#e17401", '302': "#00fdc1", '403': "#960000", '301': "#086e61", '200': "#00ff00", '401': "#fd0000", '500': "#fd59fd"}
            try:
                color = {"color":color_map[list(rel.types())[0]]}
            except:
                color = ""

            edges.append({"from": source_info["id"], "to": target_info["id"], "color": color,"label": list(rel.types())[0]})

    return vis_network(nodes, edges, physics=physics, hierarchical=hierarchical, res=res, physics_model=physics_model),