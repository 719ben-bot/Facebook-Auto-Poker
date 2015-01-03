import requests

class autoPoker(object):

   #create the autoPoke instance
   def __init__(self, email, password):

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
      homepg = self.session.post("https://m.facebook.com/login.php", headers=hdr, data=data)
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
         self.user_id = homepg_userid[1].split('" /><input type="hidden" name="c_src')[0]

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

         #go through each id and add them to postTargets
         for item in idFind[1:]:
            pokeTarget = item.split('"><div class="bh bi">')[0]
            pokeTargets.append(pokeTarget)

         #assign poke targets
         self.pokeTargets = pokeTargets


   #poke a single user
   def pokeUser(self, poke_target):

      #input for the poke
      data = ("__a=1&poke_target=" + poke_target + "&__user=" + self.user_id
      + "&__dyn=7n8ajEyl35zoSt2u6aWizGomyp9ErghyWgSmEVFLFwxBxCbzESu48jhHximmey8"
      + "szoyfw&fb_dtsg=" + self.fb_dtsg)

      #make the post request
      self.session.post("https://www.facebook.com/pokes/inline/", data=data)

      #if the user we want to poke is in the pokeTargets
      if poke_target in self.pokeTargets:

         #remove that id from the poke targets
         self.pokeTargets.remove(poke_target)


   #poke all users back
   def pokeUsersBack(self):

      #go though each of the ids in pokeTargets
      for userid in self.pokeTargets:

         #poke that user
         self.pokeUser(userid)



###usage example###

#create the autoPoker
myPoker = autoPoker("email@example.com", "password")

#get the ids of people who have poked you
myPoker.getPokeIds()

#poke those users back
myPoker.pokeUsersBack()