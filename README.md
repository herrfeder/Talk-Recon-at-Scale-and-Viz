# Talk-Recon-at-Scale-and-Viz
Talk about Recon for BugBounty/VDP and appropriate Visualisation using Jupyter and Graphs (neo4j)


| Diagram Counting Services | Diagram counting HTTP Responses over differnt tools |  
|--------------------------------------|--------------------------------------|
| ![](https://github.com/herrfeder/Talk-Recon-at-Scale-and-Viz/raw/main/examples/diagram_portscan.png) | ![](https://github.com/herrfeder/Talk-Recon-at-Scale-and-Viz/raw/main/examples/diagram_spider.png) | 

| Graph to Represent Relationship of Subdomains and IPs | Hiearchical Graph to Represent Sitemap |  
|--------------------------------------|--------------------------------------|
| ![](https://github.com/herrfeder/Talk-Recon-at-Scale-and-Viz/raw/main/examples/graph_subdomain.png) | ![](https://github.com/herrfeder/Talk-Recon-at-Scale-and-Viz/raw/main/examples/graph_url.png) | 

## Run Visualisation Notebooks

  * start neo4j Docker-Container

```
docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data neo4j
```

  * start Jupyter Environment (basically you can run whatever you want, but I recommend https://github.com/ml-tooling/ml-workspace)
  
```
docker run -d \
    -p 8080:8080 \
    --name "ml-workspace" \
    -v "${PWD}:/workspace" \
    --env AUTHENTICATE_VIA_JUPYTER="mytoken" \
    --shm-size 512m \
    --restart always \
    mltooling/ml-workspace:0.13.2
```


## Example Graphs

  * URL Hierarchical Graph: https://herrfeder.github.io/graph_url.html
  * Subdomain IP Graph: https://herrfeder.github.io/graph_subdomain.html

## Disclaimer

Any exposed vulnerability was reported and won't be exposed in any of the included data. Where specific vulnerabilities is pointed at, the associated hosts are anonymised.
