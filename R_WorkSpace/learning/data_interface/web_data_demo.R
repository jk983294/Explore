# Web Data
install.packages("RCurl")
install.packages("XML")
install.packages("stringr")
install.packages("pylr")
url <- "http://www.geos.ed.ac.uk/~weather/jcmb_ws/"							        # Read the URL.
links <- getHTMLLinks(url)															# Gather the html links present in the webpage.
filenames <- links[str_detect(links, "JCMB_2015")]								    # Identify only the links which point to the JCMB 2015 files. 
filenames_list <- as.list(filenames)												# Store the file names as a list.
downloadcsv <- function (mainurl,filename){										    # Create a function to download the files by passing the URL and filename list.
    filedetails <- str_c(mainurl,filename)
    download.file(filedetails,filename)
}
l_ply(filenames,downloadcsv,mainurl="http://www.geos.ed.ac.uk/~weather/jcmb_ws/")	# Now apply the l_ply function and save the files into the current R working directory.
