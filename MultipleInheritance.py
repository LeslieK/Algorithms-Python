class Contact:
	all_contacts = []

  	def __init__(self, name, email):
    	self.name = name
    	self.email = email
    	self.all_contacts.append(self)

class Supplier(Contact):
	def order(self, order):
  		print("If this were a real system we would send "
  			"{} order to {}".format(order, self.name))


c = Contact("Some Body", "somebody@example.net")
s = Supplier("Sup Plier", "supplier@example.net")
print(c.name, c.email, s.name, s.email)
c.all_contacts
s.order("I need pliers")

class ContactList(list):
	"extend the list data type"
	def search(self, name):
		'''
		Return all contacts that contain the search value in their name.
		'''
   		matching_contacts = []
   		for contact in self:
     		if name in contact.name:
      			matching_contacts.append(contact)
   		return matching_contacts

c1 = Contact("John A", "johna@example.net")
c2 = Contact("John B", "johnb@example.net")
c3 = Contact("Jenna C", "jennac@example.net")
[c.name for c in Contact.all_contacts.search('John')]

class LongNameDict(dict):
	"extend the dict data type"
	def longest_key(self):
  		longest = None
  		for key in self:
    		if not longest or len(key) > len(longest):
      			longest = key
    	return longest

# Commonly extended built-ins are object, list, set, dict, file, and str. 
# Numerical types such as int and float are also occasionally inherited from.

class Friend(Contact):
	def __init__(self, name, email, phone):
   		super().__init__(name, email) 	# this adds contact(name, email) to all_contacts list
   		self.phone = phone

# ALT 1: multiple inheritance
class MailSender:
	def send_mail(self, message):
  		print("Sending mail to " + self.email)
  		# Add e-mail logic here

class EmailableContact(Contact, MailSender):
	# inherits __init__ from Contact data type
	# MailSender is the mixin (like an interface in Java)
	pass

e = EmailableContact("John Smith", "jsmith@example.net")
Contact.all_contacts
e.send_mail("This is a secret email.")

# ALT 2: write a function that takes email_address as a parameter
def send_mail(emailaddress, msg):
	"function that sends email"
	print("Sending mail to " + emailaddress)

send_mail('jenna@email.com', 'This is a secret message.')

# ALT 3: define a function that takes the self parameter; 
# after Friend is created, set function as an attribute of the Friend class
def send_mail(self, msg):
	"function that sends email"
	print("Sending mail to " + emailaddress)

f = Friend('sue', 'sue@email.com', '212')
f.send_mail("This is a secret email.")


# Consider adding a home address to the Friend class.

# ALT 1: pass each of these strings as parameters into the Friend class __init__ method
class Friend(Contact):
	def __init__(self, name, email, phone, street, city, country, zipcode):
   		super().__init__(name, email) 	# this adds contact(name, email) to all_contacts list
   		self.phone = phone
   		self.street = street
   		self.city = city
   		self.country = country
   		self.zip = zipcode

# ALT 2: store strings in a tuple or dictionary and pass them into __init__ as a signle arg
address = (street, city, country, zipcode)
address = {'street' : '3 Winchester Drive', 'city' : 'East Brunswick', 'state' : 'NJ', 'zipcode' : '08816'}
class Friend(Contact):
	def __init__(self, name, email, phone, address):
   		super().__init__(name, email) 	# this adds contact(name, email) to all_contacts list
   		self.phone = phone
   		self.address = address

# ALT 3: create an Address class; pass an instance of Address class into __init__ method of Friend:
class AddressHolder:
	def __init__(self, street, city, state, zipcode):
		self.street = street
		self.city = city
		self.state = state
		self.zipcode = zipcode

# initial use of multiple inheritance: naive approach
class Friend(Contact, AddressHolder):
	def __init__(self, name, email, phone, address):
   		Contact.__init__(name, email) 	# this adds contact(name, email) to all_contacts list
   		AddressHolder.__init__(self, street, city, state, zipcode)
   		self.phone = phone

# problems
# The __init__ method from the Friend class first calls __init__ on Contact which implicitly initializes 
# the object superclass (remember, all classes derive from object). Friend then calls __init__ on AddressHolder, 
# which implicitly initializes the object superclass... again. The parent class has been set up twice.
# The thing to keep in mind with multiple inheritance is that we only want to call the "next" method in the 
# class hierarchy, not the "parent" method. ('next' method = the next method in the list of classes passed to class definition)