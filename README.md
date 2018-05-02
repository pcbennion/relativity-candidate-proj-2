## Relativity - Software Candidate Project
This readme contains the instruction for the candidates take-home project.

### Instructions:
1. Create a public Github repository. This will become your deliverable.
2. Your goal is to create a reproducable full stack solution to the following requirements:
	* I. Stand up a time series database service ( InfluxDB | Prometheus | Graphite | OpenTSDB for example )
	* II. Stand up a time series analyics dashboard ( Grafana | Kibana | Redash for example )
	* III. Find a dataset that is publicly avaliable and accesible through an API.
	* IV. Create a service that pulls from the above dataset, and stores it within the timeseries database.
	* V. Using the analytics dashboard, pull dataset information from the timeseries database.
3. Send the repository link to your Relativity point of contact. The repository should include all files necessary to set up your services, and the readme should include instructions on how to initialize your services.

#Note: The repository should only contain source code, bash scripts, or Dockerfiles required to build/install/configure any services. Deliverables will be tested on a vanilla Ubuntu 14.04 Virtual Machine.. 
