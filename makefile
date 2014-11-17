###################################################
#  ____  _    _ __  __           _      
# |  _ \| |  | |  \/  |         | |     
# | |_) | |__| | \  / | ___ __ _| | ___ 
# |  _ <|  __  | |\/| |/ __/ _` | |/ __|
# | |_) | |  | | |  | | (_| (_| | | (__ 
# |____/|_|  |_|_|  |_|\___\__,_|_|\___|
# v2.0
###################################################
# 2014 [)] Jorge I. Zuluaga, Viva la BHM!
###################################################
# Master Makefile
###################################################
USER=root
GROUP=www-data
BRANCH=$(shell bash .getbranch)

branch:
	@echo "This is branch $(BRANCH)"

clean:
	@echo "Cleaning directory..."
	@find . -name "*~" -exec rm -rf {} \;
	@find . -name "*#*" -exec rm -rf {} \;
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "screenlog*" -exec rm -rf {} \;

cleanall:
	@echo "Cleaning session directories..."
	@touch sys/seed
	@rm -r sys/*
	@cp -r web/template sys/
	@touch objs/seed
	@rm -r objs/*
	@make permissions
	@touch tmp/seed
	@rm -r tmp/*

deepclean:clean
	@echo "Cleaning temporary directories..."
	@rm -rf tmp/*
	@rm -rf repo/admin/*
	@rm -rf repo/users/*
	echo > access.log

reset:
	@echo "Resetting access.log..."
	@echo > access.log

permissions:
	@echo "Setting web permissions..."
	@chown -R $(USER):$(GROUP) .
	@chmod -R g+w .

commit:
	@echo "Committing changes to branch $(BRANCH)..."
	@git commit -am "Commit"
	@git push origin $(BRANCH)

pull:
	@echo "Getting the lattest changes from branch $(BRANCH)..."
	@git reset --hard HEAD	
	@git pull

seedtemplate:
	python BHMrun.py BHMinteraction.py sys/template interaction.conf 
	@make permissions
