# Smart-Micro-Location-Scoring

Predictive Real Estate Analysis using Graph Neural Networks

## Overview

- While location is the soul of real estate, traditional "Micro-Location" analysis is often trapped in subjective PDF reports or simple radius-based metrics
- SMLS redefines location scoring by modeling urban environments as topological graphs. Instead of asking "How many cafes are within 500m?", SMLS asks "How is this property integrated into the functional fabric of the city?" using Graph Neural Networks (GNNs)

## Key Features

- Graph-Based Connectivity: Moves beyond Euclidean distance to model actual walking/driving paths using OpenStreetMap (OSM) data
- Synergy Detection: Uses Message Passing to identify "Amenity Clusters" (e.g., the compounding value of a school next to a park vs. a school next to a highway)
- Investment Alpha: Identifies "undervalued" nodes by comparing their structural embeddings to high-performance benchmark neighborhoods
- Automated Due Diligence: Generates a multi-dimensional "Investment Score" (1-100) for any coordinate

## Tech Stack

- Deep Learning: PyTorch, PyTorch Geometric (PyG)
- Data Engineering: OSMNX, Overpass API, Pandas, GeoPandas
- Graph Metrics: NetworkX
- Visualization: Leaflet.js / Folium for geospatial plotting

## System Architecture

1. Data Acquisition & ETL

    The pipeline extracts POIs (Points of Interest) and road networks via the Overpass API

    - Nodes: Properties, Transit Hubs, Parks, Schools, Commercial zones
    - Edges: Real-world paths weighted by travel time ($t$)

2. The Model: SageConv GNN

    Utilize a GraphSAGE (Sample and Aggregate) approach to learn embeddings for nodes in large-scale city graphs. This allows the model to generalize to previously "unseen" neighborhoods

    $$h_{v}^{k} = \sigma \left( W \cdot \text{CONCAT} \left( h_{v}^{k-1}, \text{AGG} \left( \{h_{u}^{k-1}, \forall u \in \mathcal{N}(v)\} \right) \right) \right)$$

3. Scoring Engine

    The final layer maps the learned embeddings to three sub-scores:

    - Mobility Score: Transit density and network centrality
    - Lifestyle Score: Proximity to "Third Places" (cafes, gyms, libraries)
    - Risk Score: Decoupling from negative externalities (industrial noise, high-traffic arteries).

## Sample Results

Address             | Mobility  | Lifestyle | Investment Score
---------------     |---------- |-----------|------------------
"Mitte, Berlin"     | 98        | 94        | 96/100
Neukölln (Trend)    | 82        | 89        | 85/100 (High Alpha)
Spandau (Suburban)  | 45        | 30        | 38/100

## Getting Started

1. Clone the repo: git clone [https://github.com/XaverHeuser/Smart-Micro-Location-Scoring.git](https://github.com/XaverHeuser/Smart-Micro-Location-Scoring.git)
2. install Dependencies: pip install -r requirements.txt
3. Run the Scraper: python data/fetch_osm.py --city "Berlin"
4. Train the Model: python train.py --epochs 100
5. Score a Location: python score.py --address "Friedrichstraße 1, Berlin"
