# COVID-19 Reddit Information Network

## Prerequisites
Check out the file `requirements.txt` to install the correct Python modules

## File Structure
### Data Collection
Data is collected using `main.py` and stored in the `data_collection` folder, using the operations in the `data_collection_ops` folder
- The `data_preprocess_ops` folder includes operations which filter and preprocess the data collected to be used for analyzing

### Network
All things network related is in the `network creation` folder (i.e. User social network and the sentiment-weighted bipartite graph)
- The graphs created is saved in the `graph_data` folder
- Call the `get_graph(G)` function in `created_network.py` to do further analysis on the graphs
- Network analysis are stored in the `csv_data` folder
- Network and graph visualizations created in the analysis are in the `graphs` folder

### Topic Modelling and Sentiment Analysis
- LDA topic modelling related files are found in folders `topic_modelling_sentiment_analysis`, `dictionary_LDA` as well as its analysis results in `LDA_MODEL` and `csv_data`
- Some large data preprocessing and analysis from the topic model is found in the zipped folder `topic_modelling.tar.gz`
- Sentiment analysis is found in the `topic_modelling_sentiment_analysis` folder with results of the analysis are stored in the `csv_data` folder

## Notes
This project is done for the course EECS 4414 Information Networks :)

>Thalia Godbout, Razielle Dagdag, Danielle Abila and Justin So. COVID-19 Reddit Information Network.
