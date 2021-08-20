from selenium import webdriver
browser=webdriver.Firefox()
MAINPAGE='https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'
browser.get(MAINPAGE)
element1=browser.find_elements_by_xpath('/html/body/div[1]/div[3]/div/div[6]/div/div/div[4]/table')
POKEMONS=[]
for count1 in range(1,9):
	element2=element1[count1].find_elements_by_tag_name('tr')
	for count2 in range(1,len(element2)):
		element3=element2[count2].find_elements_by_tag_name('td')
		POKEMONS.append([element3[1].text,element3[2].text,element3[3].text+'/'+element3[-1].text])
browser.close()
for pokemon in POKEMONS:
	print(pokemon[0]+'\t'+pokemon[1]+'\t\t'+pokemon[2])

