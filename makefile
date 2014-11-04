###################################################
#  ____  _    _ __  __           _      
# |  _ \| |  | |  \/  |         | |     
# | |_) | |__| | \  / | ___ __ _| | ___ 
# |  _ <|  __  | |\/| |/ __/ _` | |/ __|
# | |_) | |  | | |  | | (_| (_| | | (__ 
# |____/|_|  |_|_|  |_|\___\__,_|_|\___|
# v2.0
###################################################
# 2014 (C) Jorge I. Zuluaga, Viva la BHM!
###################################################
USER=root
GROUP=www-data
BRANCH=$(shell bash .getbranch)

branch:
	@echo "This is branch $(BRANCH)"

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
	git push origin $(BRANCH)

pull:
	git reset --hard HEAD	
	git pull
