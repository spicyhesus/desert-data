# desert-data

Introduction:

This first part of the python project crawls data from the website unternehmensregister.de, a German commercial register that provides information on registered companies in Germany.
The script extracts links to the registration information, deposit tree, and documents ,storing them in separate excel files named "[type of link]_queue.csv" 
for each company on a given page of the website.
Afterwards, 3 scrapers are used for each type of crawled website.

Requirements :

Python 3.x  
requests  
BeautifulSoup  
pandas  
lxml  


Installation :

1-Clone this repository or download the ZIP file.  
2-Install the required Python packages:  
  pip install requests beautifulsoup4 pandas lxml  
  
  
Usage:

1-Open the unternehmensregister_scraper.de and execute an exteneded search action between two dates interval of your choice (the website must be in english) 
then click on the second page then back on the first page  

2-copy the url  in the url variable (outside of the trade_spider function )   

3-copy a part from the start of the url to "submitaction=pathnav&page." in the url variable (inside the while loop in the trade_spider function , keep the concatenation with the page number)  

4-copy from the start of the url to "?submication" and replace it with the link inside the embeded_url variable (keep the , a[href])  

5-change the number of pages to be crawled as the trade_spider function parameter at the last line of code   

6-after running the script 4 queue files will be created , you can now run each of the scripts   (Deposit_Tree_Scraper,Document_scraper,Pagination_Scraper,RegisterPortal_scraper)    
		Pages_queue.csv: contains links to the search result pages.  
		Register_queue.csv: contains links to register portal advice pages.  
		Deposit_tree_queue.csv: contains links to deposit tree pages.  
		Document_queue.csv: contains links to document pages.  
	
7-after the scraping finish running 4 other excel files will be created containing scraped information  
	Deposit_tree.xlsx : containing scraped deposit tree data  
	Documents.xlsx :containing scraped Documents data  
	General.xlsx : containing scraped pagination data (general data about companies)  
	Register.xlsx : containing scraped register data  

