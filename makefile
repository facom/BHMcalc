USER=root
GROUP=www-data

clean:
	find . -name "*~" -exec rm -rf {} \;
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf tmp/*
reset:
	echo > access.log

permissions:
	chown -R $(USER):$(GROUP) .
	chmod -R g+w .

commit:
	git commit -am "Commit"
	git push origin master

pull:
	git reset --hard HEAD	
	git pull
