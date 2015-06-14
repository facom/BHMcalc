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

LAST_TAG_COMMIT = $(shell git rev-list --tags --max-count=1)
LAST_TAG = $(shell git describe --tags $(LAST_TAG_COMMIT) )
TAG_PREFIX = "BHMcalc-v"
VERSION  = $(shell head VERSION)
MAJOR      = $(shell echo $(VERSION) | sed "s/^\([0-9]*\).*/\1/")
MINOR      = $(shell echo $(VERSION) | sed "s/[0-9]*\.\([0-9]*\).*/\1/")
PATCH      = $(shell echo $(VERSION) | sed "s/[0-9]*\.[0-9]*\.\([0-9]*\).*/\1/")
BUILD      = $(shell git log --oneline | wc -l | sed -e "s/[ \t]*//g")
NEXT_MAJOR_VERSION = $(shell expr $(MAJOR) + 1).0.0-b$(BUILD)
NEXT_MINOR_VERSION = $(MAJOR).$(shell expr $(MINOR) + 1).0-b$(BUILD)
NEXT_PATCH_VERSION = $(MAJOR).$(MINOR).$(shell expr $(PATCH) + 1)-b$(BUILD)

version:
	@echo "This is version $(TAG_PREFIX)$(VERSION)"
	@echo "Version: $(VERSION)"
	@echo "Last build: $(BUILD)"
	@echo "Next patch: $(NEXT_PATCH_VERSION)"
	@echo "Next minor: $(NEXT_MINOR_VERSION)"
	@echo "Next major: $(NEXT_MAJOR_VERSION)"

branch:
	@echo "This is branch $(BRANCH)"

clean:
	@echo "Cleaning directory..."
	@find . -name "*~" -exec rm -rf {} \;
	@find . -name "*#*" -exec rm -rf {} \;
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "screenlog*" -exec rm -rf {} \;
	@echo -n > logs/access.log

cleanall:clean
	@echo "Cleaning session directories..."
	@touch sys/seed
	@rm -r sys/*
	@cp -r web/template sys/
	@make permissions

deepclean:
	@echo "Deep cleaning calculator..."
	@python -Wi web/BHMdeepclean.py

reset:
	@echo "Resetting access.log..."
	@cp logs/access.log logs/access.log.save
	@echo -n > logs/access.log

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
	@git pull origin $(BRANCH)

catalogue:
	@echo "Regenerating BHM catalogue..."
	@python BHMcat.py tmp/ 1 No 0 2 -- -- html console
	@cp tmp/BHMcat.* web/template/ 
	@cp tmp/BHMcat.* sys/template/

seedtemplate:
	@echo "Seeding the template directory..."
	@python BHMrun.py BHMinteraction.py sys/template interaction.conf 
	@make permissions

packdata:
	@echo "Packing data..."
	@cd BHM/data && bash packdata.sh 
	@echo "Done."

unpackdata:
	@echo "Unpacking data..."
	@rm BHM/data/.lock
	@bash BHM/BHMinstall.sh
	@echo "Done."

decrypt:
	@echo "Decrypting Developer Guide..."
	@openssl enc -d -aes-256-cbc -in docs/DEVELOPER.enc -out docs/DEVELOPER.txt

encrypt:
	@echo "Encrypting Developer Guide..."
	@openssl enc -aes-256-cbc -in docs/DEVELOPER.txt -out docs/DEVELOPER.enc

edit:
	@emacs -nw *.py web/*.php BHM/*.py *.php makefile docs/*.txt README.md

