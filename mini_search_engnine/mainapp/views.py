from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from bs4 import BeautifulSoup
import re


# Create your views here.
def index_page(request):
    context = {
        'active_link': 'home'
    }

    return render(request, "homepage.html", context)


def omit_numbers(text):
    # Define the regular expression pattern to match [number]
    pattern = r'\[\d+\]'
    # Use re.sub() to replace all occurrences of the pattern with an empty string
    return re.sub(pattern, '', text)

def search(request):
    try:

        if request.method == 'POST':
            formdata = json.loads(request.body)
            search_query = formdata.get("searchquery") if len(formdata.get("searchquery").split(" ")) == 1 else formdata.get("searchquery").split(" ")[0].capitalize() + " " + formdata.get("searchquery").split(" ")[1].capitalize()
            print(search_query)
            url = f"https://en.wikipedia.org/wiki/{search_query}"
            response = requests.get(url)
            print("response.status_code == 200",response.status_code == 200)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # print(soup)``
                # Extract title and first paragraph
                title = soup.find('h1', id='firstHeading').text
                print(title)
                first_paragraph = soup.find('div', class_='mw-content-ltr mw-parser-output').find_all('p')
                # Extract text from each paragraph
                paragraph_texts = [paragraph.text for paragraph in first_paragraph]

                # Join the paragraphs into a single string if needed
                all_paragraphs_text = omit_numbers('\n'.join(paragraph_texts))
                # print(all_paragraphs_text)
                topic_image = ""
                main_table = soup.find('table', class_="vcard")
                
                if main_table:
                    particular_td = main_table.find('td', class_="infobox-image")
                    image = particular_td.find('img', class_="mw-file-element")
                    final_image = image.get('src')
                    topic_image = final_image

                # Contruct JSON response
                data = {
                    'title': title,
                    'paragraph': all_paragraphs_text,
                    'image': topic_image
                }
                
                return JsonResponse({'message':'success', 'status':200, 'data':data}, status=200)

            else:
                return JsonResponse({'message':'not found', 'status':200}, status=200)
        else:
            return JsonResponse({'message':'error', 'status':400}, status=400)

    except Exception as e:
        return JsonResponse({'message':'error', 'status':400}, status=400)

def contact_us(request):
    context = {
        'active_link': 'contact_us'
    }

    return render(request, 'contact_us.html', context)

def about_us(request):
    context = {
        'active_link': 'about_us'
    }

    return render(request, 'about_us.html', context)

