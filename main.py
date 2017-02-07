import webapp2
import cgi
import re

form="""
<h2>Signup</h2>
<form method="post">
<table>
<tr>
  <td class="label">
	Username
  </td>
  <td>
	<input type="text" name="username" value="%(username)s">
  </td>
  <td class="error">
	%(error_username)s
  </td>
</tr>

<tr>
  <td class="label">
	Password
  </td>
  <td>
	<input type="password" name="password" value="">
  </td>
  <td class="error">
	%(error_password)s
  </td>
</tr>

<tr>
  <td class="label">
	Verify Password
  </td>
  <td>
	<input type="password" name="verify" value="">
  </td>
  <td class="error">
	%(error_verify)s
  </td>
</tr>

<tr>
  <td class="label">
	Email (optional)
  </td>
  <td>
	<input type="text" name="email" value="%(email)s">
  </td>
  <td class="error">
	%(error_email)s
  </td>
</tr>
</table>

<input type="submit">
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
	return not email or EMAIL_RE.match(email)

class MainPage(webapp2.RequestHandler):
	def write_form(self, username="", email="", error_username="", error_email="", error_password="", error_verify=""):
		self.response.out.write(form % {"username": username,
										"email": email,
										"error_username": error_username,
										"error_email": error_email,
										"error_password": error_password,
										"error_verify": error_verify})

	def get(self):
		self.write_form()

	def post(self):
		have_error = False
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')

		params = dict(username = username,
					  email = email)

		if not valid_username(username):
			params['error_username'] = "That's not a valid username."
			have_error = True

		if not valid_password(password):
			params['error_password'] = "That wasn't a valid password."
			have_error = True
		elif password != verify:
			params['error_verify'] = "Your passwords didn't match."
			have_error = True

		if not valid_email(email):
			params['error_email'] = "That's not a valid email."
			have_error = True

		if have_error:
			self.write_form(**params)
		else:
			self.response.out.write("Thanks " + username)

app = webapp2.WSGIApplication([
	('/', MainPage)
], debug=True)
