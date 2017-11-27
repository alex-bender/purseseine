all: h j
h:
	@date +'<time class="has-text-grey" datetime="%Y-%m-%d %H:%m">%a %b %d</time>'
j:
	@date +"%a %b %d" | base64
p:
	git push origin master
