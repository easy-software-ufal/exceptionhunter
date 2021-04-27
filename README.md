# ExceptionHunter 

## Getting Started
To properly execute all steps in order to evaluate the projects, do you will need:

* A recent version of Java JRE (preferable 1.8) installed 
* A recent version of maven (preferable 3.6.0) installed
* A recent version of python (preferable 3.6.5) installed
	* pip install pymongo
	* pip install matplotlib
	* pip install pandas
	* pip install numpy
	* pip install scipy
* A recent version of MongoDB (preferable 4.0.9) installed
* At least 8GB of RAM

# Executing the tool (optional)

## Executing directly from sources

1. Import the project "exceptionhunter" in your preferred IDE. The *br.ufal.easy.exceptionhunter.ExceptionHunterMain* is the main class.
2. Import all dependencies using maven
3. In the folder ***src->main->resources*** open the file ***projects*** and configure the folder path (for your OS) where you desire to save the projects, mongoDB settings, and execution type (all tags or only the latest available).
	* e.g., "windowsProjectsRoot": "C:\\projects\\" or  "unixLikeProjectsRoot": "/home/user/projects/";
	* if you set the "tryToExtractCoverage" to true, the tool will try to query coverage data from Codecov.io and Coveralls.io websites
4.  Inside the  ***projects*** array in the ***projects*** file, you will see the following structure:
	* The key ***"active"*** specifies if the current project should be evaluated or not. If you do not want to use the project, change the ***true*** to ***false***
	* We use # instead of . (dot) in tags' name because of mongoDB restrictions.
```  
	{
		"projectName": "ghidra",
		"gitRepo": "https://github.com/NationalSecurityAgency/ghidra", 
		"active": true,  
		"description": "Ghidra is a software reverse engineering (SRE) framework", 
		"stars": 17491, 
                "tryToExtractCoverage" : true,
		"sourceRoots": [
			"all"
		], 
		"tags": {
			"Ghidra_9#0#3_build": "01/05/2019 12:08:50", 
			"Ghidra_9#0#4_build": "16/05/2019 16:36:27", 
			"Ghidra_9#0#2_build": "03/04/2019 14:38:23", 
			"Ghidra_9#0#1_build": "26/03/2019 14:46:51"
		}, 
		"createdAt": "01/03/2019 00:27:48", 
		"lastUpdatedAt": "24/09/2019 16:52:23",
		"includedAt": "24/09/2019 19:25:05",
		"size": 107426, 
		"platform": "desktop/server",
		"domain": "framework", 
		"projectOwner": "NationalSecurityAgency", 
		"contributors": 73
	},
```
5. Before running the tool, add to your execution profile the parameter ***-Xmx8192M*** to increase the Max Heap Size. Big projects require at least 8192M, but for most projects -Xmx4096M is enough.
6. Once the execution starts, each project will be downloaded to a separated folder inside the path defined in the ***projects***. This process may take a very long time if you choose to analyze all the 600 projects.
7. At the end, a ***JSON*** will be created inside of each project's folder with all collected metrics.

[comment]: <> (## Executing  from JAR)

[comment]: <> (1. In the folder ***Executable JAR***, you will see a compiled JAR with all dependencies, called ***exception-hunter-1.0.jar*** and the previous explained ***EASE2020_projects***.)

[comment]: <> (2. To execute the jar, you need to run the following command line:)

[comment]: <> (	* ***java -Xmx8192M -jar exception-hunter-1.0.jar ./projects***)
## Importing only the database	
1. If you do not want to execute the tool but want to see all data, we provide inside the folder ***\database\*** a JSON file, named ***ExceptionHunterDB***.
2. This way, you can import this JSON directly to mongoDB or open in your text editor.

# Executing the data analysis

## Scripts
Inside the folder ***EASE2020 - Data Analysis*** we provide the python scripts that we used in our data analysis.

Inside the folder ***JSS - Data Analysis*** we provide the python scripts that we used in our data analysis.
