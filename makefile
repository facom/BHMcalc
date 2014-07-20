USER=root
GROUP=www-data

clean:
	find . -name "*~" -exec rm -rf {} \;
	find . -name "*.pyc" -exec rm -rf {} \;

deepclean:clean
	rm -rf tmp/*
	rm -rf repo/admin/*
	rm -rf repo/users/*
	echo > access.log

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
