import requests
from bs4 import BeautifulSoup as bs

ideone_url = 'https://ideone.com/'
processed_ids = []
current_ids = []
s = requests.session()
inputs = []
i = 0


def main():
    j = 1
    while j in range(1, 40):
        print('-' * 80)
        ideone_recents_url = 'https://ideone.com/recent/'
        ideone_recents_url += str(j)
        r = s.get(ideone_recents_url)
        print('Scraping from: ' + ideone_recents_url)
        soup = bs(r.text, 'lxml')
        for source in soup.findAll("div", "header"):
            _id = source.find("a").text[1:]
            if _id not in processed_ids:
                current_ids.append(_id)
        j += 1
        print('Processed IDs: ' + str(len(processed_ids)))
        print('Current IDs: ' + str(len(current_ids)))
        process()


def process():
    print('-' * 80)
    print('Starting processing of this batch')
    while current_ids:
        _id = current_ids.pop()
        processed_ids.append(_id)
        sol_url = str(ideone_url + _id)
        r = s.get(sol_url)
        soup = bs(r.text, 'lxml')
        stdin = soup.find("div", id="view_stdin").find_all("div")[2].text
        stdin = stdin.replace(" ", "").replace("\n", "")
        if stdin in inputs:
            print('Match found at:' + sol_url)
    else:
        print('Finished processing this batch')
        print('Processed IDs: ' + str(len(processed_ids)))
        print('Current IDs: ' + str(len(current_ids)))


print('-' * 80)
num_inputs = int(input('Number of inputs to match with: '))
while i in range(num_inputs):
    input_to_match = input("Input to match with: ")
    input_to_match = input_to_match.replace(" ", "").replace("\n", "")
    inputs.append(input_to_match)
    i += 1
print("Matching with: ", end='')
print(str(inputs))

if __name__ == "__main__":
    main()
