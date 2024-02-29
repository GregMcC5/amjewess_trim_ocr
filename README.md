
# U-M Library American Jewess Digital Collection OCR Trimming

Gregory McCollum, February 2024




## Overview

This repository contains files associated with a project completed by Gregory McCollum at the University of Michigan Library in early 2024.

During an effort to develop level-2 (article-level) encoding on a different digital collection, I developed a method to "trim" OCR for digital collections with article-level. This trimming occurs when an article ends and another begins on the same page in a volume. In U-M digital collections system, pages like this occur twice in the collection files, once for each article on the page.

Because of this, the text of these kinds of pages will be overrepresented in search results.
Users who search the collection for words or phrases that appear on such pages will be directed to both articles, even if one of the article is not relevant to their search query.
## Collection

This workflow for trimming OCR on pages with multiple articles was developed and deployed for the [American Jewess](https://quod.lib.umich.edu/a/amjewess/) digital collection at U-M Library. *The American Jewess* was an English-language periodical for American Jewish women.

This collection was chosen because it already contained level-2, article-level encoding. Additional U-M Library collections also have article-level encoding and could benefit from this workflow as well.

As noted below, this workflow is currently configured to function at the collection-level, on a whole-collection XML file. In order to make this workflow adaptable to other collections and sustainable, more work ought to be done to adapt these scripts to item-level XML files or have the trimmed item-level XML files extracted from the collection level XML file.


## Workflow

The script *amjewess_trim.py* loads in the collection XML file (*amjewess.xml*) and for each item in the collection, accesses a list of the DIV1 tags in the item. These DIV1 tags contain the article-level information for the journal and the pages corresponding to the article. It then loops through the DIV1 tag and looks for instances where the page number of the last page of the current DIV1 tag matches the page number of the first page of the next DIV1 tag. This flags instances where two articles share a page.

This script then attempts to find the location in the page OCR where one article ends and the next begins. To do so, it loops through the lines of the page OCR and looks for a string match of the latter article's title. If not string match occurs, another pass occurs, using the best option available with fuzzy matching. This line break detection process for both of the articles' pages. (In instances where 3 or more articles appear on a page, this is necessary to already-trimmed OCR pages are not incorrectly trimmed on latter comparisons.)

Then the OCR text of the last page of the earlier article is replaced with all the lines of the OCR of that page up until the line break. The text of the first page of the latter article is replaced with the OCR of that page after the line break.

Once the DIV1 tags are successfully trimmed the BODY tag of the item is replaced with a new BODY tag containing the new, trimmed DIV1 tags. The whole collection is then rewritten as *amjewess_trimmed.xml*.
## Dependency

The fuzzy matching used to find page breaks in this workflow utilize the [*fuzzywuzzy* Python library](https://pypi.org/project/fuzzywuzzy/).

To install this, use the following command:

    pip install fuzzywuzzy

U-M Library servers should have pip already installed.
## Note

Gregory McCollum can be reached at gregmcc@umich.edu and gregmcc@uchicago.edu.
