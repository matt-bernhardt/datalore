/* HTML Scraper via jSoup
 * ---
 * This takes a URL (at url in setup() )
 * and crawls the returned markup via the pattern defined in doc.select()
 * This version then dumps the resulting content into a text file
 * for further processing with Google Refine
 */
 
// Import libraries
import org.jsoup.safety.*;
import org.jsoup.examples.*;
import org.jsoup.helper.*;
import org.jsoup.*;
import org.jsoup.parser.*;
import org.jsoup.select.*;
import org.jsoup.nodes.*;
import java.io.IOException;

// Objects
Document doc;
ArrayList<Object> articles = new ArrayList<Object>();

// JSON
JSONObject jsonOutput; // overall output file
JSONArray jsonList; // array of articles
JSONObject jsonSingle; // any single article

// Variables
String url = "http://dspace.mit.edu/handle/1721.1/49433/browse?order=DESC&rpp=20&sort_by=2&etal=-1&offset=0&type=dateissued";
String url1 = "http://dspace.mit.edu/handle/1721.1/49433/browse?order=DESC&rpp=10&sort_by=2&etal=-1&offset=";
String url2 = "&type=dateissued";

String title = "";
String handle = "";
String author = "";
String publisher = "";
String date = "";
String abstractFragment = "";

int j = 0;

void setup() {

  size(200,200);
  println("Setup started");

  // Initialize
  jsonOutput = new JSONObject();
  jsonList = new JSONArray();
  jsonSingle = new JSONObject();
  
  println("Setup finished");

  scrape(); // this builds jsonList

  jsonOutput.setJSONArray("articles",jsonList); // assign jsonList to the master object
  
  saveJSONObject(jsonOutput, "articles.json");
  
  println("Scrape finished");

}

void keyPressed() {
  // Abort operation
  println("!!! Abort - key pressed");
  exit(); // stops the program
}

void draw() {
  background(255);
}

void scrape() {
    
  for (int i = 1176; i < 1480; i = i + 1) {
    println("Page " + i);

    url = url1 + (i*10) + url2;

    jsonOutput = new JSONObject();
    jsonList = new JSONArray();
    
    scrapePage();

    jsonOutput.setJSONArray("articles",jsonList); // assign jsonList to the master object
    
    saveJSONObject(jsonOutput, "articles_" + i + ".json");

    // delay
    for (int k = 0; k < 100000; k = k + 1) {
    }
    timer(10000);

  }  
  
  println("fetched");
}

void scrapePage() {

  println("Scraping " + url);

  // wipe variables
  j = 0;  
  title = "";
  handle = "";
  author = "";
  publisher = "";
  date = "";
  abstractFragment = "";
  
  // Load a single page of the OA collection and append it to the output
  try {
    doc = Jsoup.connect(url).get();
  } catch (Exception e) {
    print(e);
    doc = null;
  }
  
  Elements articles = doc.select("ul li.ds-artifact-item");

  for (Element element : articles) {

    jsonSingle = new JSONObject();

    title = element.select("div.artifact-title a").html();
    handle = element.select("div.artifact-title a").attr("href");
    // author = element.select("span.author span").html();
    publisher = element.select("span.publisher").html();  
    date = element.select("span.date").html();
    abstractFragment = element.select("div.artifact-abstract").html();

    // jsonSingle.setInt("id",j);
    jsonSingle.setString("title",title);
    jsonSingle.setString("handle",handle);
    jsonSingle.setString("publisher",publisher);
    jsonSingle.setString("date",date);
    jsonSingle.setString("abstract",abstractFragment);
    
    jsonList.setJSONObject(j,jsonSingle); 

    j = j + 1; 
    
  }

}

void timer(int wait) {
  int now = millis();
  while (millis() < now + wait) {
  }    
}
