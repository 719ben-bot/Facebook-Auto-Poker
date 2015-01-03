import requests

#class for the users for the auto poker
class user(object):
   def __init__(self, id, name):
      self.id = id
      self.name = name

#class for error messages
class error(object):
   def __init__(self, id, name):
      self.id = id
      self.name = name

#class for the autoPoker
class autoPoker(object):

   #create the autoPoke instance
   def __init__(self, email, password):

      #create a blank blacklist
      self.blacklist = list()

      #create a blank target list
      self.pokeTargets = list()

      #create a session using requests to keep track of cookies/sessions
      self.session = requests.session()

      #header variables that we need, without these we cannot login
      hdr = {
      "POST" : "/login.php?refsrc=https%3A%2F%2Fm.facebook.com%2Fhome.php&refid=8 HTTP/1.1",
      "HOST" : "m.facebook.com",
      "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:33.0) Gecko/20100101 Firefox/33.0",
      "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
      }

      #all we need is the email/password of the user for data
      data = {
         "email" : email,
         "pass" : password
      }

      #homepage data
      homepg = self.session.post("https://m.facebook.com/login.php",
         headers=hdr, data=data)
      homepg = homepg.text.encode('utf8')

      #split up the text to get the digest and current user id
      homepg_dtsg = homepg.split("fb_dtsg")
      homepg_userid = homepg.split('<input type="hidden" name="target" value="')

      #if we have logged in
      if len(homepg_dtsg) > 1:

         #set the loggin flag
         self.loggedin = True

         #set the facebook digest
         self.fb_dtsg = homepg_dtsg[1][9:21]

         #set the user id
         self.user_id = homepg_userid[1].split('"')[0]

      #if we did not loggin correctly
      else:

         #set the loggin flag
         self.loggedin = False


   #get the users who need to be poked
   def getPokeIds(self):

      #make sure we are logged in
      if(self.loggedin):

         #request the page
         pokePage = self.session.get("https://m.facebook.com/pokes")

         #create an empty list
         pokeTargets = list()

         #split up the text to get the ids
         idFind = pokePage.text.split('id="poke_live_item_')

         #split up the text to get the names
         nameFind = pokePage.text.split('width="100" class="bl n" alt="')

         #go through each id and add them to postTargets
         for item in range(1,len(idFind)):

            #get the user to be poked id
            pokeId = idFind[item].split('"')[0]

            #get the user to be poked name
            pokeName = nameFind[item].split('"')[0]

            #create a new poke target user
            pokeTarget = user(pokeId, pokeName)

            #if the user is someone we want to poke back
            if pokeId not in self.blacklist:

               #add the target to the array
               pokeTargets.append(pokeTarget)

         #assign poke targets array
         self.pokeTargets = pokeTargets


   #poke a single user
   def pokeUser(self, poke_target):

      #if the user is not on the blacklist and logged in
      if poke_target.id not in self.blacklist and self.loggedin:

         #input for the poke
         data = ("__a=1&poke_target=" + poke_target.id + "&__user=" +
            self.user_id + "&__dyn=7n8ajEyl35zoSt2u6aWizGomyp9ErghyWgSmEV"
            + "FLFwxBxCbzESu48jhHximmey8szoyfw&fb_dtsg=" + self.fb_dtsg)

         #make the post request
         response = self.session.post("https://www.facebook.com/pokes/inline/",
            data=data).text

         #if the user we want to poke is in the pokeTargets
         if poke_target in self.pokeTargets:

            #remove that id from the poke targets
            self.pokeTargets.remove(poke_target)

         #get error messages (if there is one)
         error = response[27:34]

         #if the user has already been poked
         if error == "1769004":
            pokeError = error("1769004", "Already Poked")
            return pokeError

         #if the user is not allowed to be poked
         elif error == "1769005":
            pokeError = error("1769005", "Unauthorized Poke")
            return pokeError

         #if there is another error
         elif response[20:25] == "error":
            pokeError = error("0000000", "Unknown Error")
            return pokeError

         #if there are no errors, return the poke target
         return poke_target



   #poke all users back
   def pokeUsersBack(self):

      #create a list to return
      pokedList = list()

      #go though each of the ids in pokeTargets
      for user in self.pokeTargets:

         #poke that user
         self.pokeUser(user)

         #add the user to the pokedList
         pokedList.append(user)

      #return a list of users that was poked
      return pokedList


   #add user to the blacklist
   def addToBlacklist(self, poke_target):

      #add to the blacklist
      self.blacklist.append(poke_target)


   #remove user from the blacklist
   def removeFromBlacklist(self, poke_target):

      #if the user is in the blacklist
      if poke_target in self.blacklist:

         #remove the user
         self.blacklist.remove(poke_target)





###usage example###

#create the autoPoker
myPoker = autoPoker("email@example.com", "password")

#get the ids of people who have poked you
myPoker.getPokeIds()

#poke those users back
usersPoked = myPoker.pokeUsersBack()

#print the users poked
for user in usersPoked:
   print "Poked " + user.name