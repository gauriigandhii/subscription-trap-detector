# from django.http import JsonResponse
# from django.shortcuts import render
# from selenium import webdriver
#
#
# from selenium.webdriver.chrome.options import Options
# import time
#
#
#
#
# def scrape_and_search(request):
#    if request.method == 'GET':
#        # Get the URL from the query parameters
#        url = request.GET.get('url')
#
#
#        if url:
#            try:
#                # Initialize the webdriver (replace with the path to your Chromedriver)
#                webdriver_path = r'C:\Users\Namdev Computers\Downloads\chromedriver-win64\chromedriver-win64'
#                options = Options()
#                options.add_argument('--headless')
#
#
#                # driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
#                driver = webdriver.Chrome(options=options)
#
#
#                # Navigate to the URL
#                driver.get(url)
#
#
#                # Wait for a few seconds to ensure the page is loaded
#                time.sleep(3)
#
#
#                # Get the page source
#                page_source = driver.page_source
#
#
#                # Define specific words to search for
#                search_words = ['GoogleSearch', 'Cancellation', 'Images1', 'History', 'searchGoogle', 'हिन्दी', 'বাংলা']
#
#
#                # Search for specific words in the scraped content
#                found_words = [word for word in search_words if word in page_source]
#
#
#                # Prepare the result as a dictionary
#                result = {
#                    'url': url,
#                    'found_words': found_words,
#                    'text': page_source,
#                    'search_words': search_words
#                }
#
#
#                # Close the webdriver
#                driver.quit()
#
#
#                # Return the result as JSON response
#                return JsonResponse(request, 'sahib/results.html', {'result': result}, safe=False)
#            except Exception as e:
#                return JsonResponse({'error': f'Failed to fetch the URL: {str(e)}'}, status=400, safe=False)
#        else:
#            return JsonResponse({'error': 'Missing URL parameter'}, status=400, safe=False)
#
#
#    return JsonResponse({'error': 'Invalid request method'}, status=400)
#
# from django.shortcuts import render
#
# # Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from selenium import webdriver
from bs4 import BeautifulSoup
import re

# def extract_lines_with_found_words(text, found_words):
#     # Split the text into lines
#     lines = text.split('.')
#
#     # Initialize a list to store lines containing found_words
#     lines_with_found_words = []
#
#     for line in lines:
#         # Check if any of the found_words are present in the line (case-insensitive)
#         if any(word.lower() in line.lower() for word in found_words):
#             lines_with_found_words.append(line)
#
#     return lines_with_found_words

def highlight_found_words(text, found_words):
   # Create a regex pattern for case-insensitive and whole-word matching
   pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, found_words)) + r')\b', re.IGNORECASE)


   # Find all matches in the text
   matches = pattern.finditer(text)


   # Initialize variables for building the highlighted text
   highlighted_text = ''
   last_end = 0


   # Iterate over matches
   for match in matches:
       start, end = match.span()


       # Append the non-matching part before the current match
       highlighted_text += text[last_end:start]


       # Append the matched part with the highlighting span
       highlighted_text += f'<span class="highlight">{text[start:end]}</span>'


       # Update last_end to the end of the current match
       last_end = end


   # Append the remaining non-matching part
   highlighted_text += text[last_end:]


   return highlighted_text



def scrape_and_search(request):
    if request.method == 'GET':
        # Get the URL from the query parameters
        url = request.GET.get('url')

        if url:
            try:
                # Use Selenium to open the URL in a headless browser
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')  # Run in headless mode
                driver = webdriver.Chrome(options=options)
                driver.get(url)

                # Wait for a few seconds to ensure the page is fully loaded
                driver.implicitly_wait(5)

                # Get the HTML content from the browser
                html_content = driver.page_source

                # Close the browser
                driver.quit()

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

                # Define specific words to search for
                search_words = ['unlimited access', 'special deal', 'one-time payment', 'cancel anytime', 'limited time offer', 'exclusive access', 'free trial', 'auto-renewal', 'non-refundable', 'claim now', 'exclusive deal', 'lifetime', 'last chance', 'call free', 'best price', 'initial investment', 'limited time','cancellation']




                # Search for specific words in the scraped content
                found_words = [word for word in search_words if word in soup.get_text().lower()]
                found_lines = []
                lines = soup.get_text().split(".")
                for line in lines:
                    for word in search_words:
                        if word in line:
                            found_lines.append(line)

                highlighted_text = highlight_found_words(soup.get_text().lower(), found_words)
                # lines_with_found_words = extract_lines_with_found_words(soup.get_text().lower(), found_words)

                # Return the result as JSON
                result = {
                    'url': url,
                    'found_words': found_words,
                    'text': soup.get_text(),
                    'search_words': search_words,
                    'found_lines': found_lines,


                    'highlighted_text': highlighted_text,
                    # 'lines_with_found_words': lines_with_found_words,
                }
                return render(request, 'djangoProject/result.html', {'result': result})
            except Exception as e:
                return JsonResponse({'error': f'Failed to fetch the URL: {str(e)}'}, status=400)

        else:
            return JsonResponse({'error': 'Missing URL parameter'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


