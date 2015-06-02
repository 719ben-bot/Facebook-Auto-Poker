Facebook Auto Poker
===================

Features
--
* __The only FB Auto Poker with Two Factor Login Authentication__
* Simple login using Facebook email & password
* Choose who you poke back (Blacklist)
* Auto poking & single user poking
* Simple code design
* Python 2.7 & 3.x support

Getting started
--

Facebook Auto Poker uses the [Python Requests Library](http://docs.python-requests.org/en/latest/). To install Requests use the following command:
```bash
pip install requests
```

Now [Download the Zip](https://github.com/719Ben/Facebook-Auto-Poker/archive/master.zip) or Clone Facebook Auto Poker to your local machine. Once you have Facebook Auto Poker on you local machine, navigate to the Facebook Auto Poker directory and open up [examples.py](https://github.com/719Ben/Facebook-Auto-Poker/blob/master/examples.py). Edit the file with your login information and change the file if you would like. Run the file and you now have Facebook Auto Poker set up!

Usage of FBpoker
--

###autoPoker(email, password)
 - First Argument: Facebook username/email
 - Second Argument: Facebook password
 -Return: autoPoker object
```python
import FBpoker
myPoker = FBpoker.autoPoker("email", "pass")
```

#####.loggedin
 - Return: Bool to indicate if autoPoker object is logged into Facebook
```python
import FBpoker
myPoker = FBpoker.autoPoker("email", "pass")
if myPoker.loggin == False:
  print("you are not logged in)
```

#####.pokeUser(user_obj)
 - First Argument: User object (see below) that you want to poke
 - Return: If error: returns error object (see below) else: returns the user_obj that was poked
```python
import FBpoker
myPoker = FBpoker.autoPoker("email", "pass")
target = FBpoker.user("4", "Mark Zuckerberg", "321")
myPoker.pokeUser(target)
```

#####getPokeIds()
 - No Arguments
 - Gets all the users who have poked you. Sets them as .pokeTargets
 - Return: Array of user objects (see below) who have poked you
```python
import FBpoker
myPoker = FBpoker.autoPoker("email", "pass")
myPoker.getPokeIds()
```

#####.pokeUsersBack()
 - No Arguments
 - Pokes back all users in the .pokeTargets [set by getPokeIds()]
 - Return: a list of the users that were poked
```python
import FBpoker
myPoker = FBpoker.autoPoker("email", "pass")
myPoker.getPokeIds()
myPoker.pokeUsersBack()
```

#####addToBlacklist(poke_target)
 - First Argument: User object (see below) that you want to add to the blacklist
 - Adds a user to the blacklist of users you do not want to poke
```python
import FBpoker
myPoker = FBpoker.autoPoker("email", "pass")
target = FBpoker.user("4", "Mark Zuckerberg", "321")
FBpoker.addToBlacklist(target)
```

#####removeFromBlacklist(poke_target)
 - First Argument: User object (see below) that you want to remove from the blacklist
 - Removes a user from the blacklist of users you do not want to poke
```python
import FBpoker
myPoker = FBpoker.autoPoker("email", "pass")
target = FBpoker.user("4", "Mark Zuckerberg", "321")
FBpoker.addToBlacklist(target)
FBpoker.removeFromBlacklist(target)
```

###user(FBID, name, poke_count)
 - First Argument: Facebook user ID (http://findmyfacebookid.com/)
 - Second Argument: Facebook name
 - Third Argument: Current poke count (when creating your own user object, it does not need to be correct)
 - Return: user object that is used in blacklist creation
```python
from FBpoker import user
userMark = user("4", "Mark Zuckerberg", "321")
```

###error(id, name)
 - First Argument: Facebook error ID
 - Second Argument: Error name
```python
from FBpoker import error
userMark = error("1769004", "Already Poked")
```


To Do
--
- [X] Blacklisting
- [X] Python 3.x Support
- [X] Two Factor Login Authentication
- [X] Random Login Message Fixes (please create an issue if you get one)
- [ ] Poke Back Time Delay
