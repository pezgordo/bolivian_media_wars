# BOLIVIAN MEDIA WARS
#### Video Demo:  <URL https://youtu.be/JkqIJn0uji4>
#### Description:

https://bolivianmediawars-production.up.railway.app/

"Bolivian Media Wars" is an innovative and analytical project that arises as a result of Harvard University's CS50 course. Conceived as a web scraper, this project focuses on exploring the most relevant news websites in Bolivia to extract valuable information on specific topics. The primary purpose of this tool is to analyze and visualize trends in Bolivian media, breaking down the information into six fundamental categories: politics, security, economy, officialism, opposition, and narcotics.

The process begins with scanning various news portals to identify keywords associated with the aforementioned categories. Subsequently, the information is rigorously classified, allowing for a detailed analysis of current topics addressed by the media. This classification facilitates an understanding of each media outlet's stance and preferences in relation to different categories, contributing to a deeper interpretation of media dynamics in Bolivia.

One of the standout features of "Bolivian Media Wars" is its ability to generate interactive graphs that provide a visual representation of daily and historical media coverage on various topics. These visualizations help identify patterns, trends, and significant changes in media coverage, offering a historical perspective crucial for understanding the evolution of events in the country.

The ultimate goal of the project is to provide users with a powerful tool for media analysis in Bolivia. By examining the affinity of different media outlets with specific categories, users can gain a more precise understanding of each outlet's editorial stance and thematic orientation. This, in turn, offers valuable insights into the diversity of opinions and approaches present in the Bolivian media landscape. In summary, "Bolivian Media Wars" is not only a sophisticated technical project but also an integral tool for comprehending media dynamics in Bolivia and its implications on public opinion.




app.py - This serves as the primary application file, utilizing Dash and Plotly to construct a web app. It establishes a connection with the database (bol_wars.db) and retrieves data to generate various charts that visually represent the extracted information.


scrap.py - This Python file functions as the primary scraper responsible for gathering pertinent keywords from each media website. It stores this information in the database (bol_wars.db) in a format conducive to chart creation in the main app. The file includes the definition of keywords for each category, and if any of these keywords are identified, they are added to the database.


bol_wars.db - This database serves as the repository for all the data collected during scraping. It comprises two tables: one for categorizing and counting each identified keyword, and another for tallying the most frequently used words during the scraping process.
